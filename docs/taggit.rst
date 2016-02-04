Autocompletion for django-taggit's TaggableManager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

The :ref:`QuerySet view<queryset-view>` works here too: we're relying on
Select2 and a QuerySet of Tag objects:

.. code-block:: python

    from dal import autocomplete

    from taggit.models import Tag


    class TagAutocomplete(autocomplete.Select2QuerySetView):
        def get_queryset(self):
            # Don't forget to filter out results depending on the visitor !
            if not self.request.user.is_authenticated():
                return Tag.objects.none()

            qs = Tag.objects.all()

            if self.q:
                qs = qs.filter(name__istartswith=self.q)

            return qs

Don't forget to :ref:`register-view`.

.. note:: For more complex filtering, refer to official documentation for
          the :django:label:`queryset-api`.

Form example
============

As usual, we need a backend-aware widget that will make only selected choices
to render initially, to avoid butchering the database. As we're using a
QuerySet of Tag and Select2 in its "tag" appearance, we'll use
:py:class:`~dal_select2.widgets.TagSelect2`.

Also, we need a field that works with a queryset of Tag and use the
TaggableManager: :py:class:`~dal_taggit.fields.TaggitField`.

Finnaly, we can't use Django's ModelForm because it django-taggit's field is
made to be edited in a text input with a comma-separated list of fields, which
isn't what Select2 supports even in its tag mode. So, we'll use
:py:class:`~dal.forms.FutureModelForm`.

Example:

.. code-block:: python

    class TestForm(autocomplete.FutureModelForm):
        tags = autocomplete.TaggitField(
            required=False,
            widget=autocomplete.TagSelect2(url='your-tag-autocomplete-url'),
        )

        class Meta:
            model = TestModel
            fields = ('name',)
