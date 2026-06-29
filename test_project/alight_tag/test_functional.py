from dal.test import case
from dal_alight.test import (
    AlightCreateOption,
    AlightSelectOption,
    AlightSelectOptionMultiple,
    AlightStory,
)

from .models import TModel


class AdminTagTestCase(
    AlightStory,
    case.AdminMixin,
    case.AutocompleteTestCase,
):
    field_name = 'tags'
    model = TModel

    def setUp(self):
        super().setUp()
        self.get(url=self.get_modeladmin_url('add'))

    def test_can_add_existing_tag(self):
        story = AlightSelectOption(self)
        story.select_option('python')
        story.assert_label('python')

    def test_can_create_new_tag(self):
        story = AlightCreateOption(self)
        story.create_option('newtag')
        story.assert_label('newtag')

    def test_can_add_multiple_tags(self):
        story = AlightSelectOptionMultiple(self)
        story.select_option('django')
        story.select_option('python')
        story.assert_labels(['django', 'python'])

    def test_tags_persist_after_submit(self):
        story = AlightSelectOptionMultiple(self)
        story.select_option('django')
        story.select_option('css')
        story.assert_selection_persists(
            ['django', 'css'],
            ['django', 'css'],
        )

    def test_tags_survive_list_refresh(self):
        story = AlightSelectOptionMultiple(self)
        story.select_option('django')
        story.assert_labels(['django'])
        # Refresh the dropdown by typing a new query
        self.enter_text(self.input_selector, 'p')
        story.find_option('python')  # wait for refreshed results
        # Deck must be unchanged after dropdown refresh
        story.assert_labels(['django'])

    def test_tags_dont_appear_in_dropdown_after_selection(self):
        story = AlightSelectOptionMultiple(self)
        story.select_option('django')
        # Clear the text left by select_option, then focus to load all remaining results
        self.browser.find_by_css(self.input_selector).first.value = ''
        story.toggle_autocomplete()
        # wait for dropdown (server returns all 4, Fix 1 removes django)
        story.find_option('python')
        option_labels = [
            self.clean_label(o.text)
            for o in self.browser.find_by_css(self.option_selector)
        ]
        self.assertNotIn('django', option_labels)
        self.assertIn('python', option_labels)
