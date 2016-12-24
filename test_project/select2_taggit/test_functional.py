from dal.test import case, stories

from dal_select2.test import Select2Story

from taggit.models import Tag

from .models import TModel


class TagSelect2AdminTestMixin(Select2Story, case.AdminMixin):
    def setUp(self):
        super(TagSelect2AdminTestMixin, self).setUp()
        self.get(url=self.get_modeladmin_url('add'))
        self.fill_name()

        self.labels = [self.id() + '0', self.id() + '1']
        self.tag_model.objects.create(name=self.labels[0])

    def test_can_select_options(self):
        story = stories.SelectOptionMultiple(self)

        for option in self.labels:
            story.select_option(option)

        # assert it works with new tags
        story.assert_labels(self.labels)
        story.assert_values([self.labels[0], self.labels[1]])

        # assert tags were saved, they have a pk
        story.submit()
        story.assert_labels(self.labels)

        # With tags, values are labels
        story.assert_values(self.labels)

    def test_can_select_option_in_first_inline(self):
        story = stories.InlineSelectOptionMultiple(self, inline_number=0)

        for option in self.labels:
            story.select_option(option)

        story.assert_selection_persists(self.labels, self.labels)


class TaggitSelect2AdminTest(TagSelect2AdminTestMixin,
                             case.AutocompleteTestCase):

    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TModel
    tag_model = Tag
