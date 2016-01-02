Autocompletion for django-tagulous TagField
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note that django-tagulous provides autocompletion features. Check them out, if
it doesn't work for you or whatever reason then feel free to use dal_tagulous.

Model example
=============

Consider such a model, using `django-tagulous
<http://radiac.net/projects/django-tagulous/>`_ to handle tags for a model:

.. code-block:: python

    from django.db import models

    from tagulous.models import TagField


    class TestModel(models.Model):
        name = models.CharField(max_length=200)

        tags = TagField()

        def __str__(self):
            return self.name

View example
============

The :ref:`QuerySet view<queryset-view>` works here too: we're relying on
Select2 and a QuerySet of Tag objects. However, in django-tagulous, a specific
Tag model is made for every instance of the field. So we have to get the Tag
model class dynamically:

.. code-block:: python

    from dal import autocomplete


    class TagAutocomplete(autocomplete.Select2QuerySetView):
        def get_queryset(self):
            # Get the tag model dynamically
            Tag = TestModel.tags.tag_model

            # Don't forget to filter out results depending on the visitor !
            if not self.request.is_authenticated():
                return Tag.objects.none()

            qs = Tag.objects.all()

            if self.q:
                qs = qs.filter(name__istartswith=self.q)

            return self.q

Don't forget to :ref:`register-view`.

.. note:: For more complex filtering, refer to official documentation for
          the :django:label:`queryset-api`.

Form example
============

As usual, we need a backend-aware widget that will make only selected choices
to render initially, to avoid butchering the database. As we're using a
QuerySet of Tag and Select2 in its "tag" appearance, we'll use
:py:class:`~dal_select2.widgets.TagSelect2`.

Also, we need a field that works with a queryset of tagulous tag, and is able
to update tagulous TagField: :py:class:`~dal_tagulous.fields.TagulousField`.

Finnaly, we can't use Django's ModelForm because it django-taggit's field is
made to be edited in a text input with a comma-separated list of fields, which
isn't what Select2 supports even in its tag mode. So, we'll use
:py:class:`~dal.forms.FutureModelForm`.

Example:

.. code-block:: python

    class TestForm(autocomplete.FutureModelForm):
        tags = autocomplete.TagulousField(
            required=False,
            queryset=TestModel.test.tag_model.objects.all(),
            widget=autocomplete.TagSelect2(url='your-view-url-name'),
        )

        class Meta:
            model = TestModel
            fields = ('name',)
