from django import forms
from django import http
from django import test
from django.core.urlresolvers import reverse
from django.utils import six

from taggit.models import Tag

from .forms import TestForm
from .models import TestModel


class TagSelect2TestMixin(object):
    maxDiff = 3000

    def test_save(self):
        existing_tag = 'existing' + self.id()
        existing = self.tag.objects.create(name=existing_tag)
        new_tag = 'new' + self.id()

        form = self.form(http.QueryDict('name=%s&test=%s&test=%s' % (
            self.id(), existing.pk, new_tag)))

        instance = form.save()
        result = instance.test.all()

        new = self.tag.objects.get(name=new_tag)

        self.assertEquals(list(result), [existing, new])

        self.assertEqual(
            list(self.model.objects.get(pk=instance.pk).test.all()),
            [existing, new]
        )

    def test_validate(self):
        fixture = self.model.objects.create(name=self.id())

        form = self.form(http.QueryDict('name=%s&test=%s' % (
            self.id(), fixture.pk)))

        form.fields['test'].queryset = self.tag.objects.exclude(pk=fixture.pk)

        self.assertFalse(form.is_valid())

    def test_initial(self):
        tag = self.tag.objects.create(name='tag' + self.id())
        fixture = self.model.objects.create(name=self.id())
        fixture.test.add(tag)

        # Instanciate the modelform for that instance
        form = self.form(instance=fixture)

        # Ensure that the widget rendered right, with only the selection
        self.assertHTMLEqual(
            forms.SelectMultiple(
                choices=(
                    (tag.pk, six.text_type(tag)),
                ),
                attrs={
                    'data-autocomplete-light-create': 'true',
                    'data-autocomplete-light-function': 'select2',
                    'data-autocomplete-light-url': reverse(self.url_name),
                    'data-tags': 1,
                    'id': 'id_test',
                }
            ).render('test', value=[
                tag.pk,
            ]),
            six.text_type(form['test'].as_widget())
        )


class TaggitFormTest(TagSelect2TestMixin, test.TestCase):
    form = TestForm
    model = TestModel
    tag = Tag
    url_name = 'select2_taggit'
