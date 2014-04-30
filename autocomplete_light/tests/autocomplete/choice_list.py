from __future__ import unicode_literals

from .case import *


class AutocompleteChoiceListMock(
    autocomplete_light.AutocompleteChoiceListBase):
    limit_choices = 2

    choices = (
        (0, 'Zero'),
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (10, 'Ten'),
    )


class FormMock(forms.Form):
    x = forms.ChoiceField(choices=AutocompleteChoiceListMock.choices,
        widget=autocomplete_light.ChoiceWidget(
            autocomplete=AutocompleteChoiceListMock))


class MultipleFormMock(forms.Form):
    x = forms.MultipleChoiceField(choices=AutocompleteChoiceListMock.choices,
        widget=autocomplete_light.MultipleChoiceWidget(
            autocomplete=AutocompleteChoiceListMock))


class AutocompleteChoiceListTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteChoiceListMock

    def get_choices_for_values_tests(self):
        return (
            {
                'fixture': [1, 4],
                'expected': [
                    (4, 'Four'),
                    (1, 'One'),
                ]
            },
        )

    def get_choices_for_request_tests(self):
        return (
            {
                'fixture': make_get_request('q=t'),
                'expected': [
                    (10, 'Ten'),
                    (3, 'Three'),
                ]
            },
            {
                'fixture': make_get_request('q=2'),
                'expected': [
                    (2, 'Two'),
                ]
            },
            {
                'fixture': make_get_request(),
                'expected': [
                    (4, 'Four'),
                    (1, 'One'),
                ]
            }
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
                'fixture': make_get_request('q=t'),
                'expected': ''.join([
                    '<span data-value="10">Ten</span>',
                    '<span data-value="3">Three</span>',
                ])
            },
            {
                'fixture': make_get_request(),
                'expected': ''.join([
                    '<span data-value="4">Four</span>',
                    '<span data-value="1">One</span>',
                ])
            },
        )

    def get_widget_tests(self):
        return (
            {
                'form_class': FormMock,
                'fixture': 'x=4',
                'expected_valid': True,
                'expected_data': 4,
            },
            {
                'fixture': 'x=abc',
                'expected_valid': False,
            },
            {
                'form_class': MultipleFormMock,
                'fixture': 'x=4&x=6',
                'expected_valid': False,
            },
            {
                'fixture': 'x=4&x=10',
                'expected_valid': True,
                'expected_data': ['4', '10'],
            },
            {
                'fixture': 'x=abc&x=2',
                'expected_valid': False,
            },
        )
