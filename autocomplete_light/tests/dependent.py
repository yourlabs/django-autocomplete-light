from __future__ import unicode_literals

from .widget import WidgetTestCase


class DependentAutocompleteTestCase(WidgetTestCase):
    fixtures = ['dependent_autocomplete_test_case.json', 'initial_data.json']


class DependentAutocompleteEmptyFormTestCase(DependentAutocompleteTestCase):
    def setup_test_case(self):
        self.login()
        self.open_url('/admin/dependant_autocomplete/dummy/add/')
        self.autocomplete_name = 'country'
        self.send_keys('fra')
        self.hilighted_choice().click()

    def setUp(self):
        super(DependentAutocompleteEmptyFormTestCase, self).setUp()

        self.autocomplete_name = 'region'
        self.input().clear()

    def test_texas_not_in_france(self):
        self.send_keys('tex')
        self.unset_implicit_wait()
        self.assertTrue(len(self.autocomplete_choices()) == 0)
        self.set_implicit_wait()

    def test_alpes_in_france(self):
        self.send_keys('alp')
        self.assertTrue(len(self.autocomplete_choices()) == 2)
