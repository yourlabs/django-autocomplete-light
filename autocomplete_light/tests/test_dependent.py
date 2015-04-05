from __future__ import unicode_literals

from .test_widget import WidgetTestCase


class DependentAutocompleteTestCase(WidgetTestCase):
    fixtures = ['dependent_autocomplete_test_case.json', 'test_user.json']


class DependentAutocompleteEmptyFormTestCase(DependentAutocompleteTestCase):
    autocomplete_name = 'region'

    def setup_test_case(self):
        pass

    def select_usa(self):
        self.send_keys('united states', 'country')
        self.hilighted_choice('country').click()

    def select_france(self):
        self.send_keys('fra', 'country')
        self.hilighted_choice('country').click()

    def setUp(self):
        super(DependentAutocompleteEmptyFormTestCase, self).setUp()

        self.login()
        self.open_url('/admin/dependant_autocomplete/dummy/add/')
        self.select_france()
        self.input().clear()

    def test_texas_not_in_france(self):
        self.send_keys('tex')
        self.assertAutocompleteEmpty()

    def test_alpes_in_france(self):
        self.send_keys('alp')
        self.assertTrue(len(self.autocomplete_choices()) == 2)

    def test_change_to_different_country_after_region_select(self):
        pass

    def test_change_to_same_country_after_region_select(self):
        pass
