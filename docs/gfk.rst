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

Form example
============

To enable the use of automatic views we need to add 'dal_queryset_sequence'
 to :django:setting:`INSTALLED_APPS`.

First, we can't use Django's ModelForm because it doesn't support
non-editable fields, which GenericForeignKey is. Instead, we'll use
:py:class:`~dal.forms.FutureModelForm`.

Then we need to add the  :py:class:`~dal_queryset_sequence.fields.GenericForeignKeyModelField`
field, with model_choice as keyword: this is a list of tuple, with the models you want in the
autocompletion and the validation, and the value of the attribute of
the model you want to query in the widget searchbox.

Result:

.. code-block:: python

    from dal import autocomplete

    class TestForm(autocomplete.FutureModelForm):

        location = autocomplete.GenericForeignKeyModelField(
            model_choice=[(Country, 'country_code'), (City, 'name')],
            # Model with values to filter
            required=False,
        )

        class Meta:
            model = TestModel

Register the view for the form
==============================

In url.py:
.. code-block:: python

    from .forms import TestForm

    urlpatterns = [...]  # your regular url patterns
    urlpatterns.extend(TestForm.as_urls())

It will enable the search box to query and filter the results
