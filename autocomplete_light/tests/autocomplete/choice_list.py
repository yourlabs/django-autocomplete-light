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
                'expected': u''.join([
                    '<div data-value="10">Ten</div>',
                    '<div data-value="3">Three</div>',
                ])
            },
            {
                'fixture': make_get_request(),
                'expected': u''.join([
                    '<div data-value="4">Four</div>',
                    '<div data-value="1">One</div>',
                ])
            },
        )
