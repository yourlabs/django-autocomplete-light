from .case import *


class AutocompleteListMock(autocomplete_light.AutocompleteListBase):
    limit_choices = 2

    choices = (
        'Zero',
        'One',
        'Two',
        'Three',
        'Four',
        'Ten',
    )


class AutocompleteListTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteListMock

    def get_choices_for_values_tests(self):
        tests = (
            {
                'fixture': ['Four', 'Zero'],
            },
        )

        for test in tests:
            test['expected'] = test['fixture']

        return tests

    def get_choices_for_request_tests(self):
        return (
            {
                'fixture': make_get_request('q=t'),
                'expected': [
                    'Ten',
                    'Three',
                ]
            },
            {
                'fixture': make_get_request(),
                'expected': [
                    'Four',
                    'One',
                ]
            }
        )

    def get_validate_tests(self):
        return (
            {
                'fixture': ['One', 'Four'],
                'expected': True,
            },
            {
                'fixture': ['One', 'Hellllllo'],
                'expected': False,
            },
        )

    def get_autocomplete_html_tests(self):
        return (
            {
                'fixture': make_get_request('q=t'),
                'expected': u''.join([
                    '<div data-value="Ten">Ten</div>',
                    '<div data-value="Three">Three</div>',
                ])
            },
            {
                'fixture': make_get_request(),
                'expected': u''.join([
                    '<div data-value="Four">Four</div>',
                    '<div data-value="One">One</div>',
                ])
            },
        )

    def get_widget_tests(self):
        return []
