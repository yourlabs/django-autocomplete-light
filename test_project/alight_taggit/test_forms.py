from django import http, test
from django.urls import reverse
from taggit.models import Tag

from .forms import TForm
from .models import TModel


class TagAlightTestMixin(object):
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

        self.assertEqual(list(result), [existing, new])

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

        # Instantiate the modelform for that instance
        form = self.form(instance=fixture)

        # The alight widget wraps the <select> in <autocomplete-select>,
        # so we use assertIn checks instead of strict HTML equality.
        rendered = str(form['test'].as_widget())
        self.assertIn('autocomplete-select', rendered)
        self.assertIn(reverse(self.url_name), rendered)
        self.assertIn(str(tag), rendered)


class TaggitAlightFormTest(TagAlightTestMixin, test.TestCase):
    form = TForm
    model = TModel
    tag = Tag
    url_name = 'alight_taggit'
