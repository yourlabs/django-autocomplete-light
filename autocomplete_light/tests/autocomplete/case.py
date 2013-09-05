import unittest

from django import http
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission

import autocomplete_light


def make_get_request(query=''):
    request = http.HttpRequest()
    request.GET = http.QueryDict(query)
    return request


class AutocompleteTestCase(unittest.TestCase):
    autocomplete_mock = None

    def setUpAuth(self):
        self.user_ctype = ContentType.objects.get_for_model(User)
        self.group_ctype = ContentType.objects.get_for_model(Group)

        User.objects.all().delete()
        self.abe = User(username='Abe', email='sales@example.com')
        self.jack = User(username='Jack', email='jack@example.com')
        self.james = User(username='James', email='sales@example.com')
        self.john = User(username='John', email='sales@example.com')
        self.elton = User(username='Elton', email='elton@example.com', pk=10)

        self.abe.save()
        self.jack.save()
        self.james.save()
        self.john.save()

        Group.objects.all().delete()
        self.rockers = Group(name='rockers')
        self.bluesmen = Group(name='bluesmen')
        self.jazzmen = Group(name='jazzmen')
        self.emos = Group(name='emos', pk=10)

        self.rockers.save()
        self.bluesmen.save()
        self.jazzmen.save()
        self.emos.save()

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
            u'Got %s for test %s %s' % (result, self.__class__.__name__,
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
            u'Got %s for test %s %s' % (result, self.__class__.__name__,
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
                print self.__class__, test, self.get_widget_tests()
                raise

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
