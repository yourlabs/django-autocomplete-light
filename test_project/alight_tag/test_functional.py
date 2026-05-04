from dal.test import case, stories
from dal_alight.test import AlightStory

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
        self.browser.fill('name', 'tag_test_%s' % self.id())

    def test_can_add_existing_tag(self):
        story = stories.SelectOption(self)
        story.select_option('python')
        story.assert_label('python')

    def test_can_create_new_tag(self):
        story = stories.CreateOption(self)
        story.create_option('newtag')
        story.assert_label('newtag')

    def test_can_add_multiple_tags(self):
        story = stories.SelectOptionMultiple(self)
        story.select_option('django')
        story.select_option('python')
        story.assert_labels(['django', 'python'])

    def test_tags_persist_after_submit(self):
        story = stories.SelectOptionMultiple(self)
        story.select_option('django')
        story.select_option('css')
        story.assert_selection_persists(
            ['django', 'css'],
            ['django', 'css'],
        )
