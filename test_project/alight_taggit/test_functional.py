from taggit.models import Tag

from dal.test import case
from dal_alight.test import (
    AlightCreateOptionMultiple,
    AlightInlineSelectOptionMultiple,
    AlightSelectOptionMultiple,
    AlightStory,
)

from .models import TModel


class TagAlightAdminTestMixin(AlightStory, case.AdminMixin):
    def setUp(self):
        super().setUp()
        self.get(url=self.get_modeladmin_url('add'))
        self.fill_name()
        self.labels = [self.id() + '0', self.id() + '1']
        self.tag_model.objects.create(name=self.labels[0])
        self.tag_model.objects.create(name=self.labels[1])

    def test_can_select_options(self):
        story = AlightSelectOptionMultiple(self)
        for option in self.labels:
            story.select_option(option)
        story.assert_labels(self.labels)
        story.assert_values([self.labels[0], self.labels[1]])
        story.submit()
        story.assert_labels(self.labels)
        story.assert_values(self.labels)

    def test_can_create_new_tag(self):
        new_tag = self.id() + 'new'
        story = AlightCreateOptionMultiple(self)
        story.create_option(new_tag)
        story.assert_labels([new_tag])
        story.submit()
        story.assert_labels([new_tag])
        story.assert_values([new_tag])

    def test_can_select_option_in_first_inline(self):
        story = AlightInlineSelectOptionMultiple(self, inline_number=0)
        for option in self.labels:
            story.select_option(option)
        story.assert_selection_persists(self.labels, self.labels)


class TaggitAlightAdminTest(TagAlightAdminTestMixin, case.AutocompleteTestCase):
    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TModel
    tag_model = Tag
