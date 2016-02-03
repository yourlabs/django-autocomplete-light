from dal.test import case, stories

from dal_select2.test import Select2Story

from taggit.models import Tag

from .models import TestModel


class TagSelect2AdminTestMixin(Select2Story, case.AdminMixin):
    def setUp(self):
        super(TagSelect2AdminTestMixin, self).setUp()
        self.get(url=self.get_modeladmin_url('add'))
        self.fill_name()

    def test_can_select_options(self):
        labels = [self.id() + '0', self.id() + '1']
        pk = self.tag_model.objects.create(name=labels[0]).pk
        story = stories.SelectOptionMultiple(self)

        for option in labels:
            story.select_option(option)

        # assert it works with new tags
        story.assert_labels(labels)
        story.assert_values([pk, labels[1]])

        # assert tags were saved, they have a pk
        story.submit()
        values = self.tag_model.objects.filter(name__in=labels).values_list(
            'pk', flat=True)
        story.assert_labels(labels)
        story.assert_values(values)


class TaggitSelect2AdminTest(TagSelect2AdminTestMixin,
                             case.AutocompleteTestCase):

    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TestModel
    tag_model = Tag
