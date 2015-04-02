from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.utils.encoding import force_text

from .case import *


class AutocompleteModelMock(autocomplete_light.AutocompleteModelBase):
    limit_choices = 2
    choices = User.objects.all()
    search_fields = ('username', 'email')


class FormMock(forms.Form):
    x = forms.ModelChoiceField(queryset=AutocompleteModelMock.choices,
        widget=autocomplete_light.ChoiceWidget(
            autocomplete=AutocompleteModelMock))


class MultipleFormMock(forms.Form):
    x = forms.ModelMultipleChoiceField(queryset=AutocompleteModelMock.choices,
        widget=autocomplete_light.MultipleChoiceWidget(
            autocomplete=AutocompleteModelMock))


class AutocompleteModelTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteModelMock

    def assert_choices_equal(self, result, test):
        self.assertEqual([x.pk for x in result],
                         [x.pk for x in test['expected']])

    def get_choices_for_values_tests(self):
        return (
            {
                'fixture': [1, 4],
                'expected': [
                    self.abe,
                    self.john,
                ]
            },
        )

    def get_choices_for_request_tests(self):
        return (
            {
                'fixture': make_get_request('q=j'),
                'kwargs': {
                    'limit_choices': 5,
                },
                'expected': [
                    self.jack,
                    self.james,
                    self.john,
                ]
            },
            {
                'fixture': make_get_request('q=j'),
                'kwargs': {
                    'order_by': '-username',
                    'limit_choices': 5,
                },
                'expected': [
                    self.john,
                    self.james,
                    self.jack,
                ]
            },
            {
                'fixture': make_get_request('q=j'),
                'kwargs': {
                    'order_by': ('-email', 'username'),
                    'limit_choices': 5,
                },
                'expected': [
                    self.james,
                    self.john,
                    self.jack,
                ]
            },
            {
                'fixture': make_get_request('q=sale'),
                'expected': [
                    self.abe,
                    self.james,
                ]
            },
            {
                'fixture': make_get_request(),
                'expected': [
                    self.abe,
                    self.jack,
                ]
            },
        )

    def get_validate_tests(self):
        return (
            {
                'fixture': [1, 4],
                'expected': True,
            },
            {
                'fixture': [1, 4, 123],
                'expected': False,
            },
        )

    def get_autocomplete_html_tests(self):
        return (
            {
                'fixture': make_get_request('q=j'),
                'expected': ''.join([
                    '<span data-value="%s">%s</span>' % (
                        self.jack.pk, force_text(self.jack)),
                    '<span data-value="%s">%s</span>' % (
                        self.james.pk, force_text(self.james)),
                ])
            },
            {
                'fixture': make_get_request(),
                'expected': ''.join([
                    '<span data-value="%s">%s</span>' % (
                        self.abe.pk, force_text(self.abe)),
                    '<span data-value="%s">%s</span>' % (
                        self.jack.pk, force_text(self.jack)),
                ])
            },
        )

    def get_widget_tests(self):
        return (
            {
                'form_class': FormMock,
                'fixture': 'x=4',
                'expected_valid': True,
                'expected_data': self.john,
            },
            {
                'form_class': FormMock,
                'fixture': 'x=3&x=4',
                'expected_valid': True,
                'expected_data': self.john,
            },
            {
                'fixture': 'x=abc',
                'expected_valid': False,
            },
            {
                'form_class': MultipleFormMock,
                'fixture': 'x=4&x=2',
                'expected_valid': True,
                'expected_data': [self.jack, self.john],
            },
            {
                'fixture': 'x=abc&x=2',
                'expected_valid': False,
            },
        )
