Autocompletion for django-gm2m's GM2MField
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model example
=============

Consider such a model, using `django-gm2m
<https://django-gm2m.readthedocs.io/en/stable/>`_ to handle generic
many-to-many relations:

.. code-block:: python

    from django.db import models

    from gm2m import GM2MField


    class TestModel(models.Model):
        name = models.CharField(max_length=200)

        locations = GM2MField()

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
QuerySetSequence and Select2, we'll try
:py:class:`~dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2Multiple`
widget.

Also, we need a field that's able to use a QuerySetSequence for choices to
validate multiple models, and then update the GM2MField relations:
:py:class:`~dal_gm2m_queryset_sequence.fields.GM2MQuerySetSequenceField`.

Finnaly, we can't use Django's ModelForm because it doesn't support
non-editable fields, which GM2MField is. Instead, we'll use
:py:class:`~dal.forms.FutureModelForm`.

Example:

.. code-block:: python

    class TestForm(autocomplete.FutureModelForm):
        locations = autocomplete.GM2MQuerySetSequenceField(
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
