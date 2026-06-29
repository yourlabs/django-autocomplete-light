Upgrading from 4.0.3 to 5.0.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DAL 5.0.0 drops Django 4.2 support and requires Django 5.2 or newer.  Upgrade
Django first, then upgrade DAL without the v4 pin.

::

    pip install -U django-autocomplete-light

Python API changes
==================

If your project subclasses DAL classes or overrides DAL methods, check these
changes.

``BaseQuerySetView.post()``
---------------------------

If you override ``BaseQuerySetView.post()``, move the reusable create flow to
``self._post(request)``.

In v4, ``BaseQuerySetView.post()`` checked permissions, read ``POST['text']``,
optionally called ``validate()``, created the object, and always returned
Select2 JSON.

In v5, :py:class:`~dal.views.BaseQuerySetView` is shared by Select2 and
alight.  ``_post(request)`` only returns the created object or an early
``HttpResponse``.  Your backend-specific ``post()`` must format the final
response.

Select2-style override::

    def post(self, request, *args, **kwargs):
        result = self._post(request)
        if isinstance(result, http.HttpResponse):
            return result
        return http.JsonResponse({
            'id': self.get_result_value(result),
            'text': self.get_selected_result_label(result),
        })

For validation errors, catch ``django.core.exceptions.ValidationError`` around
``self._post(request)`` and return the response shape your frontend expects.
See ``Select2QuerySetView.post()`` and ``AlightQuerySetView.post()`` for the
built-in implementations.

If you call ``super().post()`` from a ``Select2QuerySetView`` subclass, this
still returns Select2 JSON.  If you call ``super().post()`` from a direct
``BaseQuerySetView`` subclass, update the class to inherit from
``Select2QuerySetView`` or implement ``post()`` using ``self._post()``.

Create-option hooks
-------------------

If you override ``Select2ViewMixin.get_create_option()``, keep returning a
Select2 result list, but use ``self._should_show_create(context, q)`` for the
common permission, page, empty-query, and duplicate-label checks.  Override
``BaseQuerySetView._should_show_create()`` instead if you want the same
create-option rule to apply to Select2 and alight.

v5 pattern::

    def get_create_option(self, context, q):
        if not self._should_show_create(context, q):
            return []
        return [{'id': q, 'text': 'Create "%s"' % q, 'create_id': True}]

If you set ``case_sensitive_create`` on a custom ``Select2ViewMixin`` subclass,
move it to the ``BaseQuerySetView`` / ``Select2QuerySetView`` subclass.  The
attribute is now read by ``BaseQuerySetView._should_show_create()``.

Select2 widgets
---------------

``dal_select2.widgets.Select2InitialRenderMixin`` was removed.  If your
project imports or subclasses it, remove that dependency before upgrading.

Subclass the concrete widget you need instead:

- ``Select2Multiple``
- ``ListSelect2``
- ``ModelSelect2``
- ``ModelSelect2Multiple``

Selected values are now rendered by
:py:meth:`~dal.widgets.WidgetMixin.filter_choices_to_render` for list-backed
widgets and
:py:meth:`~dal.widgets.QuerySetSelectMixin.filter_choices_to_render` for
queryset-backed widgets.

If you overrode ``render()`` only to inject initial Select2 choices, delete
that override and rely on the built-in selected-choice filtering.  If you still
need custom selected values for a list-backed widget, override
``filter_choices_to_render(selected_choices)`` instead of ``render()``.

If you override ``WidgetMixin.filter_choices_to_render()``, note that the
default implementation now keeps selected raw values even when they are absent
from ``self.choices`` by appending ``(value, value)`` pairs.  Add your own
filtering before calling ``super()`` if your project must reject unknown
selected values during rendering.

List choice fields
------------------

If you import ``dal_select2.fields.ChoiceCallable``, change the import to:

::

    from dal.fields import ChoiceCallable

``Select2ListChoiceField`` and ``Select2ListCreateChoiceField`` are still
available from ``dal_select2.fields``.

If you subclass the Select2 list fields only to reuse their generic
list/callable-choice behavior, inherit from the new backend-neutral
``dal.fields.ListChoiceField`` or ``dal.fields.ListCreateChoiceField``.  Keep
inheriting from ``dal_select2.fields.Select2ListChoiceField`` or
``Select2ListCreateChoiceField`` when the class is specifically part of a
Select2 form API.

Widget ``forward`` lists
------------------------

If you mutate ``widget.forward`` after widget construction and expected that
mutation to affect other forms sharing the same widget instance, pass the
complete ``forward=`` list when constructing each widget instead.

``WidgetMixin`` now copies ``forward`` during construction and deepcopy, so
shared mutable ``forward`` lists no longer leak between form instances.

JavaScript changes
==================

If your project only uses the bundled DAL static files through widget media,
you normally do not need JavaScript changes for existing Select2 widgets.  If
you copied DAL JavaScript into your project, override the Select2 initialization
function, or migrate widgets to alight, check these changes.

Select2 tags mode
-----------------

In v5, DAL's Select2 integration defines a ``createTag`` function for tags mode
and marks client-created tags with ``newTag: true``.  The result template shows
new tags as ``Create "value"`` while the selected value remains the raw tag
text.

If you copied or replaced ``autocomplete_light/select2.js``, add equivalent
handling:

::

    var createTagFn = null;
    if (use_tags) {
        createTagFn = function(params) {
            var term = $.trim(params.term);
            if (!term) return null;
            return {id: term, text: term, newTag: true};
        };
    }

    $element.select2({
        tags: use_tags,
        createTag: createTagFn,
        // keep your other DAL options
    });

If you override ``templateResult`` or ``templateSelection``, handle
``item.newTag`` as well as DAL's server-side ``item.create_id`` marker.
``templateResult`` should display the create label for ``newTag`` items;
``templateSelection`` should return ``item.text`` for selected ``newTag``
items.

Migrating custom JavaScript from Select2 to alight
--------------------------------------------------

The new ``dal_alight`` backend does not use jQuery or Select2.  It uses native
web components plus ``dal-django.js``.

If you migrate a widget from Select2 to alight:

- Replace Select2-specific event handlers such as ``select2:selecting`` with
  alight/web-component behavior or normal form field events.
- Do not expect autocomplete responses to be Select2 JSON.  Alight queryset and
  list views return HTML fragments containing ``data-value`` options.
- Do not expect create-on-the-fly POST responses to be JSON.  Alight create
  responses return a selected-option HTML fragment.
- Keep using DAL ``forward`` declarations in Python.  ``dal-django.js`` reads
  the same ``dal-forward-conf`` markup and appends ``forward`` data to alight
  requests.
- Keep Django admin related-object popup behavior enabled through
  ``dal-django.js`` instead of Select2-specific hooks.

For class-by-class migration from Select2 widgets and views to alight, see
``upgrade_from_select2_to_alight.rst``.

New alight Python APIs
======================

The alight backend is optional.  These APIs are exported from
``dal.autocomplete`` when their apps are installed, matching the existing
Select2 convenience import style.

``dal_alight.widgets``:

- ``ModelAlight``
- ``ModelAlightMultiple``
- ``ListAlight``
- ``TagAlight``
- ``TaggitAlight``

``dal_alight.views``:

- ``AlightQuerySetView``
- ``AlightGroupQuerySetView``
- ``AlightListView``
- ``AlightGroupListView``
- ``AlightTagAutocompleteView``

``dal_alight.fields``:

- ``AlightListChoiceField``
- ``AlightListCreateChoiceField``

``dal_alight_queryset_sequence``:

- ``AlightQuerySetSequenceView``
- ``AlightQuerySetSequenceAutoView``
- ``QuerySetSequenceAlight``
- ``QuerySetSequenceAlightMultiple``
- ``AlightGenericForeignKeyModelField``
