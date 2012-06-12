import unittest

from django import http
from django import forms

import autocomplete_light


def make_get_request(query=''):
    request = http.HttpRequest()
    request.GET = http.QueryDict(query)
    return request


class AutocompleteTestCase(unittest.TestCase):
    autocomplete_mock = None

    def assert_choices_equal(self, result, test):
        self.assertEqual(result, test['expected'])

    def test_choices_for_request(self):
        for test in self.get_choices_for_request_tests():
            mock = self.autocomplete_mock(request=test['fixture'])
            result = mock.choices_for_request()
            self.assert_choices_equal(result, test)

    def test_choices_for_values(self):
        for test in self.get_choices_for_values_tests():
            mock = self.autocomplete_mock(values=test['fixture'])
            result = mock.choices_for_values()
            self.assert_choices_equal(result, test)

    def assert_validate_success(self, result, test):
        self.assertEqual(result, test['expected'],
            u'Got %s for test %s %s' % (result, self.__class__.__name__,
                test))

    def test_validate(self):
        for test in self.get_validate_tests():
            mock = self.autocomplete_mock(values=test['fixture'])
            result = mock.validate_values()
            self.assert_validate_success(result, test)

    def test_autocomplete_html(self):
        for test in self.get_autocomplete_html_tests():
            mock = self.autocomplete_mock(request=test['fixture'])
            result = mock.autocomplete_html()
            self.assert_html_equals(result, test)

    def assert_html_equals(self, result, test):
        self.assertEqual(result, test['expected'],
            u'Got %s for test %s %s' % (result, self.__class__.__name__,
                test))

    def test_widget(self):
        form_class = None

        for test in self.get_widget_tests():
            if 'form_class' in test.keys():
                form_class = test['form_class']
            # for display
            test['form_class'] = form_class.__name__

            form = form_class(http.QueryDict(test['fixture']))
            valid = form.is_valid()

            self.assertEqual(
                valid, test['expected_valid'],
                u'Unexepected valid: %s for test %s %s' % (
                    valid, self.__class__.__name__, test)
            )

            if valid:
                data = form.cleaned_data['x']

                self.assertEqual(
                    str(data), str(test['expected_data']),
                    u'Unexepected data: %s for test %s %s' % (
                        data, self.__class__.__name__, test)
                )
