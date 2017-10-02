from dal.test import case

from dal_select2.test import Select2Story

from .models import TModel


class AdminForeignKeyTestCase(Select2Story, case.AdminMixin, case.OptionMixin,
                              case.AutocompleteTestCase):

    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TModel

    def setUp(self):
        super(AdminForeignKeyTestCase, self).setUp()
        self.get(url=self.get_modeladmin_url('add'))
        self.fill_name()

    def test_twidget_is_not_initialized(self):
        """Test that the widget didn't get initialized by select2."""
        # First check that the setup script ran in order to make sure that we
        # don't have a false positive on the next assertion.
        setup_succeeded = self.browser.evaluate_script(
            'window.__dal__tSelect2Setup')
        self.assertTrue(setup_succeeded)

        initialize_called = self.browser.evaluate_script(
            'window.__dal__tSelect2Initialized')
        self.assertFalse(initialize_called)
