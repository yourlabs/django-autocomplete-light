from django import forms
from django import http
from django import test
from django.core.urlresolvers import reverse
from django.utils import six

from tagging.models import Tag

from .forms import TestForm
from .models import TestModel


class TagSelect2TestMixin(object):
    maxDiff = 3000

    def test_save(self):
        existing_tag = 'existing' + self.id()[:30]
        self.tag.objects.create(name=existing_tag)
        new_tag = 'new' + self.id()[:30]

        form = self.form(http.QueryDict('name=%s&test=%s&test=%s' % (
            self.id(), existing_tag, new_tag)))

        instance = form.save()
        self.assertEqual(
            instance.test,
            six.text_type(',').join([existing_tag, new_tag])
        )

    def test_initial(self):
        tag = self.tag.objects.create(name='tag' + self.id()[:30])
        fixture = self.model.objects.create(name=self.id()[:30])
        fixture.test = tag.name

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
                    'data-tags': 1,
                    'id': 'id_test',
                }
            ).render('test', value=[
                six.text_type(tag),
            ]),
            six.text_type(form['test'].as_widget())
        )


class TaggitFormTest(TagSelect2TestMixin, test.TestCase):
    form = TestForm
    model = TestModel
    tag = Tag
    url_name = 'select2_tagging'
