django-taggit TaggableManager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model example
=============

Consider such a model, using `django-taggit
<https://github.com/alex/django-taggit>`_ to handle tags for a model:

.. code-block:: python

    from django.db import models

    from taggit.managers import TaggableManager


    class TestModel(models.Model):
        name = models.CharField(max_length=200)

        tags = TaggableManager()

        def __str__(self):
            return self.name

View example
============

Extend
:py:class:`~dal_alight.views.AlightTagAutocompleteView` — a convenience
subclass that overrides ``get_result_value()`` to return ``result.name``
so that :py:class:`~dal_alight.widgets.TaggitAlight` can match tags by name:

.. code-block:: python

    from dal import autocomplete

    from taggit.models import Tag


    class TagAutocomplete(autocomplete.AlightTagAutocompleteView):
        def get_queryset(self):
            if not self.request.user.is_authenticated:
                return Tag.objects.none()

            qs = Tag.objects.all()

            if self.q:
                qs = qs.filter(name__istartswith=self.q)

            return qs

Alternatively, extend :py:class:`~dal_alight.views.AlightQuerySetView`
directly and override ``get_result_value()`` yourself:

.. code-block:: python

    class TagAutocomplete(autocomplete.AlightQuerySetView):
        def get_result_value(self, result):
            return result.name

Don't forget to :ref:`register-view`.

Form example
============

Use :py:class:`~dal_alight.widgets.TaggitAlight`:

.. code-block:: python

    class TestForm(autocomplete.FutureModelForm):
        class Meta:
            model = TestModel
            fields = ('name',)
            widgets = {
                'tags': autocomplete.TaggitAlight(
                    'your-taggit-autocomplete-url'
                )
            }

