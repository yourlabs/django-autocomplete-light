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

    def test_empty_list_choices(self):
        mock = self.autocomplete_mock(request=make_get_request('q=t'))
        mock.choices = []
        mock.choices_for_request()

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
                'expected': ''.join([
                    '<span data-value="Ten">Ten</span>',
                    '<span data-value="Three">Three</span>',
                ])
            },
            {
                'fixture': make_get_request(),
                'expected': ''.join([
                    '<span data-value="Four">Four</span>',
                    '<span data-value="One">One</span>',
                ])
            },
        )

    def get_widget_tests(self):
        return []
