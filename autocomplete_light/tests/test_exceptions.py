import autocomplete_light.shortcuts as autocomplete_light
from django.test import TestCase

no_urls = ['']


class AutocompleteListMock(autocomplete_light.AutocompleteListBase):
    choices = ('a', 'b', 'c')


class AutocompleteNotRegisteredTestCase(TestCase):
    def test_no_url_empty_registry(self):
        exception = autocomplete_light.AutocompleteNotRegistered(
                'NotRegistered', autocomplete_light.AutocompleteRegistry())
        self.assertEqual(str(exception),
                'NotRegistered not registered (registry is empty)')

    def test_no_url_non_empty_registry(self):
        registry = autocomplete_light.AutocompleteRegistry()
        registry.register(AutocompleteListMock)
        exception = autocomplete_light.AutocompleteNotRegistered(
                'NotRegistered', registry)
        self.assertEqual(str(exception),
                "NotRegistered not registered, you have registered: ['AutocompleteListMock']")
