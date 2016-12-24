from dal.test import case, stories

from dal_select2.test import Select2Story

from .models import TModel


class AdminGenericForeignKeyTestCase(Select2Story, case.AdminMixin,
                                     case.ContentTypeOptionMixin,
                                     case.AutocompleteTestCase):

    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TModel

    def setUp(self):
        super(AdminGenericForeignKeyTestCase, self).setUp()
        self.get(url=self.get_modeladmin_url('add'))

    def test_can_select_option(self):
        option, ctype = self.create_option()
        story = stories.SelectOption(self)
        story.select_option(option.name)
        story.assert_selection_persists(
            '%s-%s' % (ctype.pk, option.pk),
            option.name
        )

    def test_can_select_option_in_first_inline(self):
        option, ctype = self.create_option()
        story = stories.InlineSelectOption(self, inline_number=0)
        story.select_option(option.name)
        story.assert_selection_persists(
            '%s-%s' % (ctype.pk, option.pk),
            option.name
        )

    def test_can_select_option_in_first_extra_inline(self):
        option, ctype = self.create_option()
        story = stories.InlineSelectOption(self, inline_number=3)
        story.select_option(option.name)
        story.assert_value('%s-%s' % (ctype.pk, option.pk))
