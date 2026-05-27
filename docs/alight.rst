Tutorial
~~~~~~~~

.. _alight-tutorial:

.. note:: **For demo links** to work, you need to run the :ref:`test project
   <demo-install>` on localhost.

Overview
========

``dal_alight`` is a DAL autocomplete frontend built on native
`Web Components <https://developer.mozilla.org/en-US/docs/Web/Web_Components>`_.
No jQuery or third-party JS library is required.

Key differences from the Select2 frontend:

- **No jQuery / Select2 required.**  The component is a pure web component
  (``<autocomplete-select>``) with no external library dependency.
- **The view returns HTML fragments** instead of JSON.  Each result is a
  ``<div data-value="…">…</div>`` element; the JS component reads those divs
  to build the dropdown.
- Static files served are ``dal_alight/autocomplete-light.css``,
  ``dal_alight/autocomplete-light.js``, and ``dal_alight/dal-django.js``.

Install
=======

Add ``dal_alight`` to ``INSTALLED_APPS`` **before** ``django.contrib.admin``:

.. code-block:: python

    INSTALLED_APPS = [
        'dal',
        'dal_alight',
        # 'grappelli',
        'django.contrib.admin',
        ...
    ]

For Generic Foreign Key support also add ``dal_queryset_sequence``:

.. code-block:: python

    INSTALLED_APPS = [
        'dal',
        'dal_alight',
        'dal_queryset_sequence',
        'dal_alight_queryset_sequence',  # bridges the two
        ...
    ]

.. _alight-queryset-view:

Create an autocomplete view
===========================

- Example source: `test_project/alight_foreign_key
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/test_project/alight_foreign_key/urls.py>`_
- Live demo: `/alight_foreign_key/test-autocomplete/?q=test
  <http://localhost:8000/alight_foreign_key/test-autocomplete/?q=test>`_

Use :py:class:`~dal_alight.views.AlightQuerySetView`:

.. code-block:: python

    from dal import autocomplete

    from your_countries_app.models import Country


    class CountryAutocomplete(autocomplete.AlightQuerySetView):
        def get_queryset(self):
            if not self.request.user.is_authenticated:
                return Country.objects.none()

            qs = Country.objects.all()

            if self.q:
                qs = qs.filter(name__istartswith=self.q)

            return qs

Register the view
=================

.. code-block:: python

    from django.urls import path

    from your_countries_app.views import CountryAutocomplete

    urlpatterns = [
        path(
            'country-autocomplete/',
            CountryAutocomplete.as_view(),
            name='country-autocomplete',
        ),
    ]

The simplest registration passes the model directly without a custom view class:

.. code-block:: python

    from dal import autocomplete
    from your_countries_app.models import Country

    urlpatterns = [
        path(
            'country-autocomplete/',
            autocomplete.AlightQuerySetView.as_view(model=Country),
            name='country-autocomplete',
        ),
    ]

.. danger:: As with all DAL views, the URL is public by default.  Always check
            permissions in ``get_queryset()``.

Use the view in a Form widget
=============================

ForeignKey (single select)
--------------------------

Use :py:class:`~dal_alight.widgets.ModelAlight` for a ``ForeignKey`` field:

.. code-block:: python

    from dal import autocomplete
    from django import forms


    class PersonForm(forms.ModelForm):
        class Meta:
            model = Person
            fields = ('__all__',)
            widgets = {
                'birth_country': autocomplete.ModelAlight(url='country-autocomplete')
            }

ManyToManyField (multi select)
------------------------------

Use :py:class:`~dal_alight.widgets.ModelAlightMultiple` for a
``ManyToManyField``:

.. code-block:: python

    widgets = {
        'visited_countries': autocomplete.ModelAlightMultiple(url='country-autocomplete')
    }

Initial values on edit forms
----------------------------

:py:class:`~dal_alight.widgets.ModelAlight` and
:py:class:`~dal_alight.widgets.ModelAlightMultiple` inject the currently
selected object(s) into the ``<select>`` options at render time so they
appear pre-selected without an extra AJAX call.

Automation with djhacker
------------------------

- Example source: `test_project/alight_djhacker_formfield
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/test_project/alight_djhacker_formfield/urls.py>`_
- Live demo: `/admin/alight_djhacker_formfield/tmodel/add/
  <http://localhost:8000/admin/alight_djhacker_formfield/tmodel/add/>`_

.. code-block:: python

    import djhacker  # pip install djhacker
    from django import forms

    djhacker.formfield(
        Person.birth_country,
        forms.ModelChoiceField,
        widget=autocomplete.ModelAlight(url='country-autocomplete')
    )

Using autocompletes in the admin
================================

Register a ``ModelAdmin`` with your custom form:

.. code-block:: python

    from django.contrib import admin

    from your_person_app.models import Person
    from your_person_app.forms import PersonForm


    class PersonAdmin(admin.ModelAdmin):
        form = PersonForm

    admin.site.register(Person, PersonAdmin)

Inlines work the same way:

.. code-block:: python

    class PersonInline(admin.TabularInline):
        model = Person
        form = PersonForm

Using autocompletes outside the admin
=====================================

- Example source: `test_project/alight_outside_admin
  <https://github.com/yourlabs/django-autocomplete-light/tree/master/test_project/alight_outside_admin>`_
- Live demo: `/alight_outside_admin/
  <http://localhost:8000/alight_outside_admin/>`_

Include ``{{ form.media }}`` — the widget's ``media`` property loads
``autocomplete-light.js`` and ``dal-django.js`` automatically:

.. literalinclude:: ../test_project/alight_outside_admin/templates/alight_outside_admin/alight_outside_admin.html

Creation of new choices
=======================

- Example source: `test_project/alight_one_to_one
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/test_project/alight_one_to_one/urls.py>`_
- Live demo: `/admin/alight_one_to_one/tmodel/add/
  <http://localhost:8000/admin/alight_one_to_one/tmodel/add/>`_

Set ``create_field`` on the view to enable on-the-fly object creation:

.. code-block:: python

    urlpatterns = [
        path(
            'country-autocomplete/',
            CountryAutocomplete.as_view(create_field='name'),
            name='country-autocomplete',
        ),
    ]

When no exact match exists the view appends a
``<div data-create data-value="…">Create "…"</div>`` element to its response.
Selecting it triggers a POST to the same URL; the view creates the object and
returns the rendered HTML label directly (a ``<div data-value="…">…</div>``
fragment), which the component inserts into the selection deck.

Add ``validate_create=True`` to run ``full_clean()`` before saving:

.. code-block:: python

    CountryAutocomplete.as_view(create_field='name', validate_create=True)

.. include:: _forward.rst

Autocompleting from a list of strings
======================================

- Example source: `test_project/alight_list
  <https://github.com/yourlabs/django-autocomplete-light/tree/master/test_project/alight_list>`_

Use :py:class:`~dal_alight.views.AlightListView` when results come from a
plain Python list rather than a QuerySet:

.. code-block:: python

    class FruitAutocomplete(autocomplete.AlightListView):
        def get_list(self):
            return ['apple', 'mango', 'apricot', 'orange']

Register it as a named URL, then use :py:class:`~dal_alight.widgets.ListAlight`
in your form:

.. code-block:: python

    widget = autocomplete.ListAlight(url='fruit-autocomplete')

To allow creating values that are not in the list, define a ``create`` method
on the view:

.. code-block:: python

    class FruitAutocomplete(autocomplete.AlightListView):
        def get_list(self):
            return ['apple', 'mango', 'apricot', 'orange']

        def create(self, text):
            return text  # return the stored value

And use :py:class:`~dal_alight.fields.AlightListCreateChoiceField` in the form
so the submitted value passes validation:

.. code-block:: python

    from dal import autocomplete


    class FruitForm(forms.ModelForm):
        fruit = autocomplete.AlightListCreateChoiceField(
            choice_list=['apple', 'mango', 'apricot', 'orange'],
            widget=autocomplete.ListAlight(url='fruit-autocomplete'),
        )

For a static list that only accepts existing values, use
:py:class:`~dal_alight.fields.AlightListChoiceField` instead.

Grouped results
===============

QuerySet-backed groups
----------------------

Use :py:class:`~dal_alight.views.AlightGroupQuerySetView` to render results
grouped by a related field.  Set ``group_by_related`` to the name of the
ForeignKey whose target model provides the group label, and optionally
``related_field_name`` (default ``'name'``) for the label attribute:

.. code-block:: python

    class CountryAutocomplete(autocomplete.AlightGroupQuerySetView):
        group_by_related = 'continent'
        related_field_name = 'name'

        def get_queryset(self):
            return Country.objects.all()

List-based groups
-----------------

Use :py:class:`~dal_alight.views.AlightGroupListView` for grouped string lists.
Return ``(group_name, item)`` pairs from ``get_list()``:

.. code-block:: python

    class FruitAutocomplete(autocomplete.AlightGroupListView):
        def get_list(self):
            return [
                ('Tropical', 'mango'),
                ('Tropical', 'papaya'),
                ('Temperate', 'apple'),
                ('Temperate', 'pear'),
            ]

Items with ``group=None`` are rendered without a group header.

Tags support
============

Free-text tags (no taggit)
--------------------------

Use :py:class:`~dal_alight.widgets.TagAlight` for a comma-separated tag field
not backed by a taggit model.  The widget stores tags as a comma-separated
string.

django-taggit integration
-------------------------

- Example source: `test_project/alight_taggit
  <https://github.com/yourlabs/django-autocomplete-light/tree/master/test_project/alight_taggit>`_
- Live demo: `/admin/alight_taggit/tmodel/add/
  <http://localhost:8000/admin/alight_taggit/tmodel/add/>`_

The view works with ``AlightQuerySetView`` using the tag name as the result
value:

.. code-block:: python

    from dal import autocomplete
    from taggit.models import Tag


    class TagAutocomplete(autocomplete.AlightQuerySetView):
        def get_result_value(self, result):
            return result.name

        def get_queryset(self):
            if not self.request.user.is_authenticated:
                return Tag.objects.none()
            qs = Tag.objects.all()
            if self.q:
                qs = qs.filter(name__istartswith=self.q)
            return qs

In the form use :py:class:`~dal_alight.widgets.TaggitAlight`:

.. code-block:: python

    class TestForm(autocomplete.FutureModelForm):
        class Meta:
            model = TestModel
            fields = ('name',)
            widgets = {
                'tags': autocomplete.TaggitAlight('your-taggit-autocomplete-url')
            }

Generic Foreign Key support
===========================

- Example source: `test_project/alight_generic_foreign_key
  <https://github.com/yourlabs/django-autocomplete-light/tree/master/test_project/alight_generic_foreign_key>`_
- Live demo: `/admin/alight_generic_foreign_key/tmodel/add/
  <http://localhost:8000/admin/alight_generic_foreign_key/tmodel/add/>`_

See :doc:`gfk` for the model setup.

Automatic view using :py:class:`~dal_alight_queryset_sequence.fields.AlightGenericForeignKeyModelField`:

.. code-block:: python

    from dal import autocomplete
    from django.contrib.auth.models import Group


    class TestForm(autocomplete.FutureModelForm):
        location = autocomplete.AlightGenericForeignKeyModelField(
            model_choice=[
                (Country, 'name'),
                (City, 'name', [('language', 'spoken_language')]),
            ],
        )

        class Meta:
            model = TestModel

Register the auto-generated URL in ``urls.py``:

.. code-block:: python

    from .forms import TestForm

    urlpatterns += TestForm.as_urls()

Manual view using ``GenericForeignKeyModelField`` with explicit widget and view:

.. code-block:: python

    from dal import autocomplete
    from dal_alight_queryset_sequence.views import AlightQuerySetSequenceView
    from dal_alight_queryset_sequence.widgets import QuerySetSequenceAlight


    class TestForm(autocomplete.FutureModelForm):
        location = autocomplete.GenericForeignKeyModelField(
            model_choice=[(Country,), (City,)],
            widget=QuerySetSequenceAlight,
            view=AlightQuerySetSequenceView,
        )

        class Meta:
            model = TestModel

Class reference
===============

.. list-table:: Views
   :header-rows: 1

   * - Class
     - Description
   * - :py:class:`~dal_alight.views.AlightQuerySetView`
     - QuerySet-backed autocomplete, returns HTML fragments
   * - :py:class:`~dal_alight.views.AlightGroupQuerySetView`
     - QuerySet-backed, results grouped by a related field
   * - :py:class:`~dal_alight.views.AlightListView`
     - Autocomplete from a Python list
   * - :py:class:`~dal_alight.views.AlightGroupListView`
     - Grouped autocomplete from a Python list
   * - :py:class:`~dal_alight_queryset_sequence.views.AlightQuerySetSequenceView`
     - Multi-model Generic FK view (``dal_alight_queryset_sequence``)

.. list-table:: Widgets
   :header-rows: 1

   * - Class
     - Description
   * - :py:class:`~dal_alight.widgets.ModelAlight`
     - Single select, QuerySet-backed (ForeignKey)
   * - :py:class:`~dal_alight.widgets.ModelAlightMultiple`
     - Multi select, QuerySet-backed (ManyToManyField)
   * - :py:class:`~dal_alight.widgets.Alight`
     - Single select, arbitrary choices
   * - :py:class:`~dal_alight.widgets.AlightMultiple`
     - Multi select, arbitrary choices
   * - :py:class:`~dal_alight.widgets.ListAlight`
     - Single select, list-backed
   * - :py:class:`~dal_alight.widgets.TagAlight`
     - Free-text tag widget (comma-separated)
   * - :py:class:`~dal_alight.widgets.TaggitAlight`
     - django-taggit integration
   * - :py:class:`~dal_alight_queryset_sequence.widgets.QuerySetSequenceAlight`
     - Single select, multi-model GFK (``dal_alight_queryset_sequence``)
   * - :py:class:`~dal_alight_queryset_sequence.widgets.QuerySetSequenceAlightMultiple`
     - Multi select, multi-model GFK (``dal_alight_queryset_sequence``)

.. list-table:: Form fields
   :header-rows: 1

   * - Class
     - Description
   * - :py:class:`~dal_alight.fields.AlightListChoiceField`
     - ChoiceField validated against a list or callable
   * - :py:class:`~dal_alight.fields.AlightListCreateChoiceField`
     - Like above, allows on-the-fly created values
   * - :py:class:`~dal_alight_queryset_sequence.fields.AlightGenericForeignKeyModelField`
     - Auto-wired GFK field (``dal_alight_queryset_sequence``)
