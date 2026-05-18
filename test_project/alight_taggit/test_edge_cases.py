import urllib.parse

from django import http, test
from taggit.models import Tag

from .forms import TForm
from .models import TModel


def _form(name, tags, instance=None):
    qs = urllib.parse.urlencode([('name', name)] + [('test', t) for t in tags])
    return TForm(http.QueryDict(qs), instance=instance)


class TaggitAlightEdgeCaseTest(test.TestCase):
    def test_unicode_tag_name(self):
        tag = Tag.objects.create(name='тëst-юникод')
        form = _form('m', ['тëst-юникод'])
        self.assertTrue(form.is_valid(), form.errors)
        instance = form.save()
        self.assertEqual(list(TModel.objects.get(pk=instance.pk).test.all()), [tag])

    def test_html_special_chars_in_tag(self):
        tag = Tag.objects.create(name='a <b> & c')
        form = _form('m', ['a <b> & c'])
        self.assertTrue(form.is_valid(), form.errors)
        instance = form.save()
        self.assertEqual(list(TModel.objects.get(pk=instance.pk).test.all()), [tag])

    def test_very_long_tag(self):
        long_name = 'x' * 99
        tag = Tag.objects.create(name=long_name)
        form = _form('m', [long_name])
        self.assertTrue(form.is_valid(), form.errors)
        instance = form.save()
        self.assertEqual(list(TModel.objects.get(pk=instance.pk).test.all()), [tag])

    def test_tag_removal(self):
        keep = Tag.objects.create(name='keep-tag')
        drop = Tag.objects.create(name='drop-tag')
        instance = TModel.objects.create(name='m')
        instance.test.add(keep, drop)
        form = _form('m', ['keep-tag'], instance=instance)
        self.assertTrue(form.is_valid(), form.errors)
        updated = form.save()
        self.assertEqual(list(TModel.objects.get(pk=updated.pk).test.all()), [keep])
