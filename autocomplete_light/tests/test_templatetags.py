from __future__ import unicode_literals

from collections import OrderedDict

from autocomplete_light.templatetags. \
    autocomplete_light_tags import autocomplete_light_data_attributes
from django.test import TestCase


class DataAttributesTestCase(TestCase):
    def test_without_prefix(self):
        tests = (
            {
                'fixture': {
                    'foo': 'bar',
                },
                'expected': 'data-foo="bar"',
            },
            {
                'fixture': OrderedDict([
                    ('foo', 'bar'),
                    ('test_underscore', 'example'),
                ]),
                'expected': 'data-foo="bar" data-test-underscore="example"',
            },
            {
                'fixture': {
                    'foo': 'bar',
                },
                'prefix': 'autocomplete-',
                'expected': 'data-autocomplete-foo="bar"',
            },
        )

        for test in tests:
            result = autocomplete_light_data_attributes(test['fixture'],
                test.get('prefix', ''))
            self.assertEqual(result, test['expected'],
                'Got %s for %s' % (result, test))
