from dal.test import case
from dal_alight.test import AlightInlineSelectOption, AlightSelectOption, AlightStory

from .models import TModel


class AdminForeignKeyTestCase(
    AlightStory,
    case.AdminMixin,
    case.OptionMixin,
    case.AutocompleteTestCase,
):
    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TModel

    def setUp(self):
        super().setUp()
        self.get(url=self.get_modeladmin_url('add'))
        self.fill_name()

    def test_can_select_option(self):
        option = self.create_option()
        story = AlightSelectOption(self)
        story.select_option(option.name)
        story.assert_selection_persists(option.pk, option.name)

    def test_can_select_option_in_first_inline(self):
        option = self.create_option()
        story = AlightInlineSelectOption(self, inline_number=0)
        story.select_option(option.name)
        story.assert_selection(option.pk, option.name)

    def test_can_select_option_in_first_extra_inline(self):
        option = self.create_option()
        story = AlightInlineSelectOption(self, inline_number=3)
        story.select_option(option.name)
        story.assert_selection(option.pk, option.name)

    def test_can_unselect_option(self):
        option = self.create_option()
        story = AlightSelectOption(self)
        story.select_option(option.name)
        story.submit()
        story.clear_option()
        story.assert_selection_persists('', '')

    def test_initial_value_prefilled_on_edit(self):
        """A previously saved value must appear in the deck on the edit form."""
        option = self.create_option()
        # Save a record with the option selected.
        instance = self.model.objects.create(name='edit_me', test=option)
        self.get(url=self.get_modeladmin_url('change', object_id=instance.pk))
        story = AlightSelectOption(self)
        story.assert_label(option.name)
        story.assert_value(option.pk)
