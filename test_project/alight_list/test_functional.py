from dal.test import case
from dal_alight.test import AlightCreateOption, AlightStory, AlightSelectOption

from .models import TModel


class AdminListTestCase(
    AlightStory,
    case.AdminMixin,
    case.AutocompleteTestCase,
):
    field_name = 'test'
    model = TModel

    def setUp(self):
        super().setUp()
        self.get(url=self.get_modeladmin_url('add'))
        self.browser.fill('name', 'test_%s' % self.id())

    def test_can_select_from_list(self):
        story = AlightSelectOption(self)
        story.select_option('apple')
        story.assert_selection_persists(
            'apple', 'apple',
        )

    def test_can_create_new_item(self):
        story = AlightCreateOption(self)
        new_value = 'starfruit'
        story.create_option(new_value)
        story.assert_selection_persists(new_value, new_value)

    def test_suggestions_filter_by_query(self):
        story = AlightSelectOption(self)
        story.toggle_autocomplete()
        self.enter_text(self.input_selector, 'ap')
        story.assert_suggestion_labels_are(['apple', 'apricot'])
