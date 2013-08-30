import unittest

from django.test import TransactionTestCase
from django.contrib.contenttypes.models import ContentType

from cities_light.models import Country, City

from gfk_autocomplete.forms import TaggedItemForm
from optionnal_gfk_autocomplete.forms import OptionnalTaggedItemForm


class GenericModelFormTestCase(unittest.TestCase):
    def setUp(self):
        self.country, c = Country.objects.get_or_create(name='Countryname')
        self.city, c = City.objects.get_or_create(country=self.country,
            name=u'Paris')

    def tearDown(self):
        self.country.delete()
        self.city.delete()

    def test_model_form(self):
        tests = (
            {
                'content_object': self.city,
                'tag': 'foo',
                'valid': True,
                'form_class': TaggedItemForm,
            },
            {
                'tag': 'bar',
                'valid': False,
                'form_class': TaggedItemForm,
            },
            {
                'content_object': self.city,
                'tag': 'foo',
                'valid': True,
                'form_class': OptionnalTaggedItemForm,
            },
            {
                'tag': 'bar',
                'valid': True,
                'form_class': OptionnalTaggedItemForm,
            },
        )

        for test in tests:
            if 'data' not in test.keys():
                test['data'] = {'tag': test.get('tag', None)}

                if 'content_object' in test.keys():
                    test['data']['content_object'] = u'%s-%s' % (
                        ContentType.objects.get_for_model(test['content_object']).pk,
                        test['content_object'].pk)

            form = test['form_class'](test['data'])
            self.assertEqual(form.is_valid(), test['valid'])
            if test['valid']:
                result = form.save()
                self.assertEqual(test['tag'], result.tag)

                if 'content_object' in test.keys():
                    self.assertEqual(test['content_object'],
                        result.content_object)
