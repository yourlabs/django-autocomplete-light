from dal.test import case, stories

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

    def test_can_select_option(self):
        option = self.create_option()
        story = stories.SelectOption(self)
        story.select_option(option.name)
        story.assert_selection_persists(option.pk, option.name)

    def test_can_select_option_in_first_inline(self):
        option = self.create_option()
        story = stories.InlineSelectOption(self, inline_number=0)
        story.select_option(option.name)
        story.assert_selection(option.pk, option.name)

    def test_can_select_option_in_first_extra_inline(self):
        option = self.create_option()
        story = stories.InlineSelectOption(self, inline_number=3)
        story.select_option(option.name)
        story.assert_selection(option.pk, option.name)

    def test_can_change_selected_option(self):
        option = self.create_option()
        story = stories.RenameOption(self)
        story.select_option(option.name)

        add_keys = 'new name'
        story.rename_option(option.name, add_keys)

        story.assert_label(add_keys)
        story.assert_value(option.pk)
        story.assert_selection_persists(option.pk, add_keys)

    def test_can_add_another_option(self):
        story = stories.AddAnotherOption(self)

        name = 'add another %s' % self.id()
        story.add_another(name)

        story.assert_selection_persists(
            self.model.objects.get(name=name).pk, name)

    def test_can_unselect_option(self):
        option = self.create_option()
        story = stories.SelectOption(self)
        story.select_option(option.name)
        story.submit()

        story.clear_option()

        story.assert_selection_persists('', '')
