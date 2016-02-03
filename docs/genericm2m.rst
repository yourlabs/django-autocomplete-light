Autocompletion for django-generic-m2m's RelatedObjectsDescriptor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model example
=============

Consider such a model, using `django-generic-m2m
<https://github.com/coleifer/django-generic-m2m>`_ to handle generic
many-to-many relations:

.. code-block:: python

    from django.db import models

    from genericm2m.models import RelatedObjectsDescriptor


    class TestModel(models.Model):
        name = models.CharField(max_length=200)

        locations = RelatedObjectsDescriptor()

        def __str__(self):
            return self.name

View example
============

The :ref:`generic-autocomplete-view` works here too: we're relying on Select2
and QuerySetSequence again.

Form example
============

As usual, we need a backend-aware widget that will make only selected choices
to render initially, to avoid butchering the database. As we're using a
QuerySetSequence and Select2 for multiple selections, we'll try
:py:class:`~dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2Multiple`
widget.

Also, we need a field that's able to use a QuerySetSequence for choices to
validate multiple models, and then update the RelatedObjectsDescriptor
relations:
:py:class:`~dal_genericm2m_queryset_sequence.fields.GenericM2MQuerySetSequenceField`.

Finnaly, we can't use Django's ModelForm because it doesn't support
non-editable fields, which RelatedObjectsDescriptor is. Instead, we'll use
:py:class:`~dal.forms.FutureModelForm`.

Example:

.. code-block:: python

    class TestForm(autocomplete.FutureModelForm):
        locations = autocomplete.GenericM2MQuerySetSequenceField(
            queryset=autocomplete.QuerySetSequence(
                Country.objects.all(),
                City.objects.all(),
            ),
            required=False,
            widget=autocomplete.QuerySetSequenceSelect2Multiple(
                'location-autocomplete'),
        )

        class Meta:
            model = TestModel
            fields = ('name',)
