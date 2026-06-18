Upgrading from 3.12.1 to 4.0.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DAL 4.0.3 is a breaking upgrade from 3.12.1.  It focuses on supported
runtimes and removes unmaintained integration packages.

Runtime requirements
====================

Upgrade your project to Python 3.11 or newer and Django 4.2 or newer before
upgrading DAL.

::

    pip install -U "django-autocomplete-light<5"

Optional integrations
=====================

Install the extras your project uses explicitly.

::

    pip install -U "django-autocomplete-light[gfk]<5"
    pip install -U "django-autocomplete-light[tags]<5"
    pip install -U "django-autocomplete-light[nested]<5"

Removed packages
================

Remove these packages from ``INSTALLED_APPS`` and from Python imports.  They
are no longer shipped in DAL 4.0.3:

- ``dal_genericm2m``
- ``dal_genericm2m_queryset_sequence``
- ``dal_gm2m``
- ``dal_gm2m_queryset_sequence``
- ``dal_select2_tagging``
- ``dal_legacy_static``

The ``genericm2m`` extra was removed.  Generic foreign key support remains
available through ``django-autocomplete-light[gfk]`` and
``dal_queryset_sequence``.  django-taggit support remains available through
``django-autocomplete-light[tags]`` and ``dal_select2_taggit``.

Python API changes
==================

If your project subclasses DAL classes or overrides DAL methods, check these
changes.

Removed integration imports
---------------------------

If you import from ``dal_genericm2m``, ``dal_genericm2m_queryset_sequence``,
``dal_gm2m``, ``dal_gm2m_queryset_sequence``, ``dal_select2_tagging``, or
``dal_legacy_static``, remove those imports.  DAL v4 does not ship replacement
classes for these packages.  Migrate generic object autocompletes to
``dal_contenttypes`` / ``dal_queryset_sequence`` or keep custom compatibility
code in your project.

If you use ``from dal import autocomplete`` as a convenience import, remove
references to the deleted re-exports:

- ``GenericM2MQuerySetSequenceField``
- ``GM2MQuerySetSequenceField``
- ``TaggingSelect2``

The contenttypes field mixins are now re-exported when ``dal_contenttypes`` and
``django.contrib.contenttypes`` are installed:

- ``ContentTypeModelFieldMixin``
- ``ContentTypeModelMultipleFieldMixin``
- ``GenericModelMixin``

``FutureModelForm``
-------------------

If you subclass :py:class:`~dal.forms.FutureModelForm` and override ``save()``
only for the old Django 1.8/1.9 compatibility behavior, delete that override
and use Django's ``ModelForm.save()`` behavior.  DAL v4 no longer overrides
``FutureModelForm.save()``.

If you override ``FutureModelForm._save_m2m()``, update any
``opts.virtual_fields`` fallback.  v4 iterates over
``chain(opts.many_to_many, opts.private_fields)``.  The ``opts.virtual_fields``
compatibility path was removed with support for old Django versions.

Widget rendering
----------------

If you override ``WidgetMixin.render_options()``, move that logic to
:py:meth:`~dal.widgets.WidgetMixin.optgroups` or to ``render()``.
``render_options()`` was a Django < 1.10 compatibility hook and is no longer
called by supported Django versions.

If your widget subclass passes ``attrs=None`` or mutates ``attrs`` before
calling ``WidgetMixin.__init__()``, keep doing so safely: v4 reads the
placeholder with ``(kwargs.get("attrs") or {}).get("data-placeholder")``.
You no longer need a local workaround for ``attrs=None``.

Selected choice rendering
-------------------------

If you override
:py:meth:`~dal.widgets.QuerySetSelectMixin.filter_choices_to_render` or
``ModelSelect2Multiple.filter_choices_to_render()``, note that
``ModelSelect2Multiple`` now preserves the submitted Select2 order by ordering
the queryset with ``Case`` / ``When``.  Keep that ordering in custom
multiple-queryset widgets if display order matters.

If you overrode ``render()`` on ``Select2Multiple``, ``ListSelect2``,
``ModelSelect2``, or ``ModelSelect2Multiple`` only to make initial AJAX values
render as selected options, remove that override and use the v4 built-in
behavior.  These widgets now include
``dal_select2.widgets.Select2InitialRenderMixin``.

If you subclass Select2 widgets and want the v4 initial-value behavior, include
``Select2InitialRenderMixin`` before ``Select2WidgetMixin`` in the base-class
list, following the built-in widgets.

::

    class MyWidget(Select2InitialRenderMixin, Select2WidgetMixin, forms.Select):
        pass

List choice fields
------------------

If you subclass ``Select2ListChoiceField`` or call ``ChoiceCallable()``
directly, callable/list choices are normalized to tuples in v4.  Code that
expected list instances from ``ChoiceCallable`` should accept tuples instead.

Old compatibility branches
--------------------------

If you use Python 2 / old-Django compatibility imports from DAL internals,
remove those branches.  Examples:

- ``django.core.urlresolvers.reverse``
- callable ``user.is_authenticated()``
- ``django.contrib.admin.utils.lookup_needs_distinct``
- ``backports.functools_lru_cache``

DAL v4 is Python 3.11+ and Django 4.2+ only.

JavaScript changes
==================

If your project only uses the bundled DAL static files through widget media,
you normally do not need JavaScript changes.  If you copied DAL JavaScript into
your project or override DAL's Select2 initialization, check these changes.

HTMX swaps
----------

DAL v4 listens for ``htmx:afterSettle`` and initializes autocomplete widgets in
the swapped content, including the root element from ``e.detail.elt``.

If your project has custom HTMX code that manually calls
``window.__dal__initialize`` after every swap, keep it only for custom cases
that DAL cannot see.  Otherwise it can initialize the same widget twice.

The v4 initialization pattern is:

::

    document.addEventListener('htmx:afterSettle', function (e) {
        if (window.__dal__initialize && window.django && django.jQuery) {
            var $root = django.jQuery(e.detail.elt);
            $root.find('[data-autocomplete-light-function]')
                .addBack('[data-autocomplete-light-function]')
                .excludeTemplateForms()
                .each(window.__dal__initialize);
        }
    });

Select2 placeholder and clear button
------------------------------------

If you copied or replaced ``autocomplete_light/select2.js``, update your
Select2 options to match v4:

::

    var isRequired = $element.is('[required]');
    var placeholderText = (
        $element.attr('data-placeholder') || (!isRequired ? ' ' : '')
    );

    $element.select2({
        placeholder: placeholderText,
        allowClear: !isRequired,
        // keep your other DAL options
    });

This keeps Select2's clear button disabled for required fields and gives
optional fields a space placeholder when no explicit ``data-placeholder`` is
configured.  That fallback is needed by Select2's clear-button behavior.

Removed legacy static package
-----------------------------

If templates or build scripts refer to files from ``dal_legacy_static``, remove
those references.  The package is not shipped in v4.

Builds from source
==================

If your deployment or packaging scripts build DAL from source, switch from
``setup.py`` entry points to the PEP 517 build backend.

::

    python -m build

What to test after upgrading
============================

After upgrading, test forms that render existing Select2 values, multiple
Select2 submissions, clearable placeholders, HTMX swaps, and any custom
``attrs=None`` widget construction.  These areas changed between 3.12.1 and
4.0.3.
