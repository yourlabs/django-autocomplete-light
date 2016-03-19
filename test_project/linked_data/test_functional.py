from dal.test import case, stories
from dal.test.utils import OwnedFixtures

from dal_select2.test import Select2Story

from .models import TestModel


class AdminLinkedDataTest(Select2Story,
                          case.AdminMixin,
                          case.OptionMixin,
                          case.AutocompleteTestCase):
    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TestModel

    def setUp(self):
        super(AdminLinkedDataTest, self).setUp()

        if not getattr(self, 'fixtures', None):
            self.fixtures = OwnedFixtures()
            self.fixtures.install_fixtures(self.model)

        self.get(url=self.get_modeladmin_url('add'))
        self.prefix = ''

    def set_owner(self, value):
        self.browser.execute_script(
            '$("[name=%s]").val(%s)' % (self.prefix + 'owner', value)
        )

    def test_filter_options(self, story=None):
        if story is None:
            story = stories.SelectOption(self)

        story.toggle_autocomplete()

        expected = self.model.objects.values_list('name', flat=True)
        self.assertEqual(sorted(expected),
                         sorted(story.get_suggestions_labels()))

        self.set_owner(self.fixtures.test.pk)
        story.refresh_autocomplete()

        expected = self.model.objects.filter(
            owner=self.fixtures.test).values_list('name', flat=True)
        self.assertEqual(sorted(expected),
                         sorted(story.get_suggestions_labels()))

        self.set_owner(self.fixtures.other.pk)
        story.refresh_autocomplete()

        expected = self.model.objects.filter(
            owner=self.fixtures.other).values_list('name', flat=True)
        self.assertEqual(sorted(expected),
                         sorted(story.get_suggestions_labels()))

    def test_filter_option_in_first_inline(self):
        self.prefix = '%s-%s-' % (self.inline_related_name, 0)
        story = stories.InlineSelectOption(self, inline_number=0)
        self.test_filter_options(story)

    def test_can_select_option_in_first_extra_inline(self):
        story = stories.InlineSelectOption(self, inline_number=3)
        self.prefix = '%s-%s-' % (self.inline_related_name, 3)
        self.test_filter_options(story)
