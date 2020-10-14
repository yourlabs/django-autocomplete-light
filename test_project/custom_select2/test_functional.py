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
