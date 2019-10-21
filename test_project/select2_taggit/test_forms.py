import django
from django import forms
from django import http
from django import test
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

import six

from taggit.models import Tag

from .forms import TForm
from .models import TModel


class TagSelect2TestMixin(object):
    maxDiff = 3000

    def test_save(self):
        existing_tag = 'existing' + self.id()
        existing = self.tag.objects.create(name=existing_tag)
        new_tag = 'new' + self.id()

        form = self.form(http.QueryDict('name=%s&test=%s&test=%s' % (
            self.id(), existing_tag, new_tag)))

        instance = form.save()
        result = instance.test.all()

        new = self.tag.objects.get(name=new_tag)

        self.assertEquals(list(result), [existing, new])

        self.assertEqual(
            list(self.model.objects.get(pk=instance.pk).test.all()),
            [existing, new]
        )

    def test_multi_words_tag(self):
        multi_words_tag = self.tag.objects.create(name='multi words')
        form = self.form(http.QueryDict('name=%s&test=%s' % (
            self.id(), multi_words_tag)))

        instance = form.save()

        self.assertEqual(
            list(self.model.objects.get(pk=instance.pk).test.all()),
            [multi_words_tag, ]
        )

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
                    (six.text_type(tag), six.text_type(tag)),
                ),
                attrs={
                    'data-autocomplete-light-function': 'select2',
                    'data-autocomplete-light-url': reverse(self.url_name),
                    'data-autocomplete-light-language': 'en',
                    'data-tags': ',',
                    'id': 'id_test',
                }
            ).render('test', value=[
                six.text_type(tag),
            ], attrs={'required': django.VERSION >= (1, 10)}),
            six.text_type(form['test'].as_widget())
        )


class TaggitFormTest(TagSelect2TestMixin, test.TestCase):
    form = TForm
    model = TModel
    tag = Tag
    url_name = 'select2_taggit'
