from dal.test import case, stories

from dal_select2.test import Select2Story

from .models import TModel


class AdminGenericM2MBase(object):
    field_name = 'test'
    inline_related_name = 'inline_test_models'

    def setUp(self):
        super(AdminGenericM2MBase, self).setUp()
        self.get(url=self.get_modeladmin_url('add'))
        self.fill_name()

    def test_can_select_option(self):
        option0, ctype0 = self.create_option()
        option1, ctype1 = self.create_option()
        story = stories.SelectOptionMultiple(self)
        story.select_option(option0.name)
        story.select_option(option1.name)
        story.assert_selection_persists(
            (
                '%s-%s' % (ctype0.pk, option0.pk),
                '%s-%s' % (ctype1.pk, option1.pk)
            ),
            (
                option0.name,
                option1.name,
            ),
        )


class AdminGenericM2MTestCase(AdminGenericM2MBase,
                              Select2Story,
                              case.AdminMixin,
                              case.ContentTypeOptionMixin,
                              case.AutocompleteTestCase):
    model = TModel
