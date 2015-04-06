from __future__ import unicode_literals

import autocomplete_light.shortcuts as autocomplete_light  # noqa
from django import forms  # noqa
from django import http
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from six import text_type

from ...example_apps.autocomplete_test_case_app.models import Group, User


def make_get_request(query=''):
    request = http.HttpRequest()
    request.GET = http.QueryDict(query)
    return request


class AutocompleteTestCase(TestCase):
    autocomplete_mock = None
    fixtures = ['autocomplete_model_test_case']

    def setUp(self):
        self.user_ctype = ContentType.objects.get_for_model(User)
        self.group_ctype = ContentType.objects.get_for_model(Group)

        self.rockers = Group.objects.get(name='rockers')
        self.bluesmen = Group.objects.get(name='bluesmen')
        self.jazzmen = Group.objects.get(name='jazzmen')
        self.emos = Group.objects.get(name='emos')

        self.abe = User.objects.get(username='Abe')
        self.jack = User.objects.get(username='Jack')
        self.james = User.objects.get(username='James')
        self.john = User.objects.get(username='John')
        self.elton = User.objects.get(username='Elton')

    def assert_choices_equal(self, result, test):
        self.assertEqual(result, test['expected'],
                'Unexpected result %s\nTest: %s' % (result, test))

    def test_choices_for_request(self):
        if not hasattr(self, 'get_choices_for_request_tests'):
            return

        for test in self.get_choices_for_request_tests():
            mock = self.autocomplete_mock(request=test['fixture'])
            for k, v in test.get('kwargs', {}).items():
                setattr(mock, k, v)
            result = mock.choices_for_request()
            self.assert_choices_equal(list(result), test)

    def test_choices_for_values(self):
        if not hasattr(self, 'get_choices_for_values_tests'):
            return

        for test in self.get_choices_for_values_tests():
            mock = self.autocomplete_mock(values=test['fixture'])
            result = mock.choices_for_values()
            self.assert_choices_equal(result, test)

    def assert_validate_success(self, result, test):
        self.assertEqual(result, test['expected'],
            'Got %s for test %s %s' % (result, self.__class__.__name__,
                test))

    def test_validate(self):
        if not hasattr(self, 'get_validate_tests'):
            return

        for test in self.get_validate_tests():
            mock = self.autocomplete_mock(values=test['fixture'])
            result = mock.validate_values()
            self.assert_validate_success(result, test)

    def test_autocomplete_html(self):
        if not hasattr(self, 'get_autocomplete_html_tests'):
            return

        for test in self.get_autocomplete_html_tests():
            mock = self.autocomplete_mock(request=test['fixture'])
            result = mock.autocomplete_html()
            self.assert_html_equals(result, test)

    def assert_html_equals(self, result, test):
        self.assertEqual(result, test['expected'],
            'Got %s for test %s %s' % (result, self.__class__.__name__,
                test))

    def test_widget(self):
        form_class = None

        if not hasattr(self, 'get_widget_tests'):
            return

        for test in self.get_widget_tests():
            if 'form_class' in test.keys():
                form_class = test['form_class']
            # for display
            test['form_class'] = form_class.__name__

            form = form_class(http.QueryDict(test['fixture']))
            try:
                valid = form.is_valid()
            except TypeError:
                print(self.__class__, test, self.get_widget_tests())
                raise

            self.assertEqual(
                valid, test['expected_valid'],
                'Unexepected valid: %s for test %s %s' % (
                    valid, self.__class__.__name__, test)
            )

            if valid:
                data = form.cleaned_data['x']

                self.assertEqual(text_type(data), text_type(test['expected_data']),
                    'Unexepected data: %s for test %s %s' % (
                        data, self.__class__.__name__, test)
                )
