django-autocomplete-light tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overview
========

Autocompletes are based on 3 moving parts:

- widget compatible with the model field, does the initial rendering,
- javascript widget initialization code, to trigger the autocomplete,
- and a view used by the widget script to get results from.

.. _queryset-view:

Create an autocomplete view
===========================

- Example source code: `test_project/select2_foreign_key
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/test_project/select2_foreign_key/urls.py>`_
- Live demo: `/select2_foreign_key/test-autocomplete/?q=test
  <http://dal-yourlabs.rhcloud.com/select2_foreign_key/test-autocomplete/?q=test>`_

The only purpose of the autocomplete view is to serve relevant suggestions for
the widget to propose to the user. DAL leverages Django's `class based views
<https://docs.djangoproject.com/es/1.9/topics/class-based-views/>`_
and `Mixins <https://en.wikipedia.org/wiki/Mixin>`_ to for code reuse.

.. note:: Do **not** miss the `Classy Class-Based Views
          <http://ccbv.co.uk/>`_ website which helps a lot to work with
          class-based views in general.

In this tutorial, we'll learn to make autocompletes backed by a
:django:term:`QuerySet`. Suppose we have a Country :django:term:`Model`
which we want to provide a `Select2 <https://select2.github.io/>`_ autocomplete
widget for in a form. If a users types an "f" it would propose "Fiji",
"Finland" and "France", to authenticated users only:

.. image:: img/autocomplete.png

The base view for this is :py:class:`~dal_select2.views.Select2QuerySetView`.

.. code-block:: python

    from dal import autocomplete

    from your_countries_app.models import Country


    class CountryAutocomplete(autocomplete.Select2QuerySetView):
        def get_queryset(self):
            # Don't forget to filter out results depending on the visitor !
            if not self.request.user.is_authenticated():
                return Country.objects.none()

            qs = Country.objects.all()

            if self.q:
                qs = qs.filter(name__istartswith=self.q)

            return qs

.. note:: For more complex filtering, refer to official documentation for
          the :django:label:`queryset-api`.

.. _register-view:

Register the autocomplete view
==============================

Create a :django:label:`named url<naming-url-patterns>` for the view, ie:

.. code-block:: python

    from your_countries_app.views import CountryAutocomplete

    urlpatterns = [
        url(
            r'^country-autocomplete/$',
            CountryAutocomplete.as_view(),
            name='country-autocomplete',
        ),
    ]

Ensure that the url can be reversed, ie::

    ./manage.py shell
    In [1]: from django.core.urlresolvers import reverse

    In [2]: reverse('country-autocomplete')
    Out[2]: u'/country-autocomplete/'

.. danger:: As you might have noticed, we have just exposed data through a
            public URL. Please don't forget to do proper permission checks in
            get_queryset.

Use the view in a Form widget
=============================

You should be able to open the view at this point:

.. image:: img/view.png

We can now use the autocomplete view our Person form, for its ``birth_country``
field that's a ``ForeignKey``. So, we're going to :django:label:`override the
default ModelForm fields<modelforms-overriding-default-fields>`, to use a
widget to select a Model with Select2, in our case by passing the name of the
url we have just registered to :py:class:`~dal_select2.widgets.ModelSelect2`.

One way to do it is by overriding the form field, ie:

.. code-block:: python

    from dal import autocomplete

    from django import forms


    class PersonForm(forms.ModelForm):
        birth_country = forms.ModelChoiceField(
            queryset=Country.objects.all(),
            widget=autocomplete.ModelSelect2(url='country-autocomplete')
        )

        class Meta:
            model = Person
            fields = ('__all__')


Another way to do this is directly in the ``Form.Meta.widgets`` dict, if
overriding the field is not needed:

.. code-block:: python

    from dal import autocomplete

    from django import forms


    class PersonForm(forms.ModelForm):
        class Meta:
            model = Person
            fields = ('__all__')
            widgets = {
                'birth_country': autocomplete.ModelSelect2(url='country-autocomplete')
            }

If we need the country autocomplete view for a widget used for a ManyToMany
relation instead of a ForeignKey, with a model like that:

.. code-block:: python

    class Person(models.Model):
        visited_countries = models.ManyToManyField('your_countries_app.country')

Then we would use the :py:class:`~dal_select2.widgets.ModelSelect2Multiple`
widget, ie.:

.. code-block:: python

    widgets = {
        'visited_countries': autocomplete.ModelSelect2Multiple(url='country-autocomplete')
    }

Passing options to select2
==========================

`Select2
<https://select2.github.io/>`_ supports a bunch of `options
<https://select2.github.io/options.html>`_. These options may be
`set in data-* attributes
<https://select2.github.io/options.html#data-attributes>`_. For example:

.. code-block:: python

    # Instanciate a widget with a bunch of options for select2:
    autocomplete.ModelSelect2(
        url='select2_fk',
        attrs={
            # Set some placeholder
            'data-placeholder': 'Autocomplete ...',
            # Only trigger autocompletion after 3 characters have been typed
            'data-minimum-input-length': 3,
        },
    )

Using autocompletes in the admin
================================

We can make ModelAdmin to :django:label:`use our
form<admin-custom-validation>`, ie:

.. code-block:: python

    from django.contrib import admin

    from your_person_app.models import Person
    from your_person_app.forms import PersonForm


    class PersonAdmin(admin.ModelAdmin):
        form = PersonForm
    admin.site.register(Person, PersonAdmin)

Note that this also works with inlines, ie:

.. code-block:: python

    class PersonInline(admin.TabularInline):
        model = Person
        form = PersonForm

Using autocompletes outside the admin
=====================================

- Example source code: `test_project/select2_outside_admin
  <https://github.com/yourlabs/django-autocomplete-light/tree/master/test_project/select2_outside_admin>`_,
- Live demo: `/select2_outside_admin/
  <http://dal-yourlabs.rhcloud.com/select2_outside_admin/>`_.

Ensure that jquery is loaded before ``{{ form.media }}``:

.. literalinclude:: ../test_project/select2_outside_admin/templates/select2_outside_admin.html

Overriding javascript code
==========================

We need javascript initialization for the widget both when:

- the page is loaded,
- a widget is dynamically added, ie. with formsets.

This is handled by ``autocomplete.init.js``, which is going to trigger an event
called ``autocompleteLightInitialize`` on any HTML element with attribute
``data-autocomplete-light-function`` both on page load and DOM node insertion.
It also keeps track of initialized elements to prevent double-initialization.

Take ``dal_select2`` for example, it is initialized by
``dal_select2/static/autocomplete_light/select2.js`` as such:

.. code-block:: javascript

    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function() {
        // do select2 configuration on $(this)
    })

This example defines a callback that does ``// do select2 configuration on
$(this)`` when the ``autocompleteLightInitialize`` event is triggered on any
element with an attribute ``data-autocomplete-light-function`` of value
``select2``. Select2 Widgets have an :py:attr:`autocomplete_function` of value
``select2``, and that's rendered as the value of the
``data-autocomplete-light-function`` attribute.

So, you can replace the default callback by doing two things:

- change the Widget's ``autocomplete_function`` attribute,
- add a callback for the ``autocompleteLightInitialize`` event for that
  function,

Example widget:

.. code-block:: python

    class YourWidget(ModelSelect2):
        autocomplete_function = 'your-autocomplete-function'

Example script:

.. code-block:: javascript

    $(document).on(
        'autocompleteLightInitialize',
        '[data-autocomplete-light-function=your-autocomplete-function]',
    function() {
        // do your own script setup here
    })

Creation of new choices in the autocomplete form
================================================

- Example source code: `test_project/select2_one_to_one
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/test_project/select2_one_to_one/urls.py>`_,
- Live demo: `/admin/select2_one_to_one/testmodel/add/
  <http://dal-yourlabs.rhcloud.com/admin/select2_one_to_one/testmodel/add/>`_,

The view may provide an extra option when it can't find any result matching the
user input. That option would have the label ``Create "query"``, where
``query`` is the content of the input and corresponds to what the user typed
in. As such:

.. image:: img/create_option.png

This allows the user to create objects on the fly from within the AJAX
widget. When the user selects that option, the autocomplete script will make a
POST request to the view. It should create the object and return the pk, so the
item will then be added just as if it already had a PK:

.. image:: img/created_option.png

To enable this, first the view must know how to create an object given only
``self.q``, which is the variable containing the user input in the view. Set
the ``create_field`` view option to enable creation of new objects from within
the autocomplete user interface, ie:

.. code-block:: python

    urlpatterns = [
        url(
            r'^country-autocomplete/$',
            CountryAutocomplete.as_view(create_field='name'),
            name='country-autocomplete',
        ),
    ]

This way, the option 'Create "Tibet"' will be available if a user inputs
"Tibet" for example. When the user clicks it, it will make the post request to
the view which will do ``Country.objects.create(name='Tibet')``. It will be
included in the server response so that the script can add it to the widget.

Note that creating objects is only allowed to staff users with add permission
by default.

Filtering results based on the value of other fields in the form
================================================================

- Example source code: `test_project/select2_linked_data
  <https://github.com/yourlabs/django-autocomplete-light/tree/master/test_project/linked_data>`_.
- Live demo: `Admin / Linked Data / Add
  <http://dal-yourlabs.rhcloud.com/admin/linked_data/testmodel/add/>`_.

In the live demo, create a TestModel with ``owner=None``, and another with
``owner=test`` (test being the user you log in with). Then, in in a new form,
you'll see both options if you leave the owner select empty:

.. image:: img/all.png

But if you select ``test`` as an owner, and open the autocomplete again, you'll
only see the option with ``owner=test``:

.. image:: img/mine.png

Let's say we want to add a "Continent" choice field in the form, and filter the
countries based on the value on this field. We then need the widget to pass the
value of the continent field to the view when it fetches data. We can use the
``forward`` widget argument to do this:

.. code-block:: python

    class PersonForm(forms.ModelForm):
        continent = forms.ChoiceField(choices=CONTINENT_CHOICES)

        class Meta:
            model = Person
            fields = ('__all__')
            widgets = {
                'birth_country': autocomplete.ModelSelect2(url='country-autocomplete'
                                                           forward=['continent'])
            }

DAL's Select2 configuration script will get the value fo the form field named
``'continent'`` and add it to the autocomplete HTTP query. This will pass the
value for the "continent" form field in the AJAX request, and we can then
filter as such in the view:

.. code-block:: python

    class CountryAutocomplete(autocomplete.Select2QuerySetView):
        def get_queryset(self):
            if not self.request.is_authenticated():
                return Country.objects.none()

            qs = Country.objects.all()

            continent = self.forwarded.get('continent', None)

            if continent:
                qs = qs.filter(continent=continent)

            if self.q:
                qs = qs.filter(name__istartswith=self.q)

            return qs

Clearing autocomplete on forward field change
---------------------------------------------

You can use the ``$.getFormPrefix()`` jQuery plugin used by DAL to clear the
``birth_country`` autocomplete widget from the above example when the
``continent`` field changes with such a snippet:

.. code-block:: javascript

    $(document).ready(function() {
        // Bind on continent field change
        $(':input[name$=continent]').on('change', function() {
            // Get the field prefix, ie. if this comes from a formset form
            var prefix = $(this).getFormPrefix();

            // Clear the autocomplete with the same prefix
            $(':input[name=' + prefix + 'birth_country]').val(null).trigger('change');
        });
    });

To autoload the script with the form, you can use `Form.Media
<https://docs.djangoproject.com/en/1.9/topics/forms/media/#media-on-forms>`_.
