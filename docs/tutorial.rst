django-autocomplete-light tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Overview
========

Autocompletes are based on 3 moving parts:

- widget, does the initial rendering,
- javascript widget initialization code, to trigger the autocomplete,
- and a view used by the widget script to get results from.

.. _queryset-view:

Create an autocomplete view
===========================

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
"Finland" and "France", to authenticated users only. The base view for this is
:py:class:`~dal_select2.views.Select2QuerySetView`.


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
            'country-autocomplete/$',
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
        visited_countries = models.ManyToMany('your_countries_app.country')

Then we would use the :py:class:`~dal_select2.widgets.ModelSelect2Multiple`
widget, ie.:

.. code-block:: python

    widgets = {
        'visited_countries': autocomplete.ModelSelect2Multiple(url='country-autocomplete')
    }

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

Ensure that jquery is loaded before ``{{ form.media }}``, see the
``select2_outside_admin`` example in ``test_project`` for an example:

.. literalinclude:: ../test_project/select2_outside_admin/templates/select2_outside_admin.html
