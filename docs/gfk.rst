Autocompletion for GenericForeignKey
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model example
=============

Consider such a model:

.. code-block:: python

    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.db import models


    class TestModel(models.Model):
        name = models.CharField(max_length=200)

        content_type = models.ForeignKey(
            'contenttypes.ContentType',
            null=True,
            blank=True,
            editable=False,
        )

        object_id = models.PositiveIntegerField(
            null=True,
            blank=True,
            editable=False,
        )

        location = GenericForeignKey('content_type', 'object_id')

        def __str__(self):
            return self.name

.. _generic-autocomplete-view:

View example for QuerySetSequence and Select2
=============================================

We'll need a view that will provide results for the select2 frontend, and that
uses QuerySetSequence as the backend. Let's try
:py:class:`~dal_select2_queryset_sequence.views.Select2QuerySetSequenceView`
for this:

.. code-block:: python

    from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView

    from queryset_sequence import QuerySetSequence

    from your_models import Country, City


    class LocationAutocompleteView(Select2QuerySetSequenceView):
        def get_queryset(self):
            countries = Country.objects.all()
            cities = City.objects.all()

            if self.q:
                countries = countries.filter(continent__incontains=self.q)
                cities = cities.filter(country__name__icontains=self.q)

            # Aggregate querysets
            qs = QuerySetSequence(countries, cities)

            if self.q:
                # This would apply the filter on all the querysets
                qs = qs.filter(name__icontains=self.q)

            # This will limit each queryset so that they show an equal number
            # of results.
            qs = self.mixup_querysets(qs)

            return qs

Register the view in urlpatterns as usual, ie.:

.. code-block:: python

    from .views import LocationAutocompleteView

    urlpatterns = [
        url(
            r'^location-autocomplete/$',
            LocationAutocompleteView.as_view(),
            name='location-autocomplete'
        ),
    ]

Form example
============

As usual, we need a backend-aware widget that will make only selected choices
to render initially, to avoid butchering the database. As we're using a
QuerySetSequence and Select2, we'll try
:py:class:`~dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2`
widget.

Also, we need a field that's able to use a QuerySetSequence for choices to do
validation on a single model choice, we'll use
:py:class:`~dal_queryset_sequence.fields.QuerySetSequenceModelField`.

Finnaly, we can't use Django's ModelForm because it doesn't support
non-editable fields, which GenericForeignKey is. Instead, we'll use
:py:class:`~dal.forms.FutureModelForm`.

Result:

.. code-block:: python

    class TestForm(autocomplete.FutureModelForm):
        location = dal_queryset_sequence.fields.QuerySetSequenceModelField(
            queryset=autocomplete.QuerySetSequence(
                Country.objects.all(),
                City.objects.all(),
            ),
            required=False,
            widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('location-autocomplete'),
        )

        class Meta:
            model = TestModel
