from dal.test import case, stories
from dal.test.utils import OwnedFixtures

from dal_select2.test import Select2Story

from .models import TestModel


class AdminLinkedDataTest(Select2Story, case.AdminMixin, case.OptionMixin,
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

    def test_filtered_options(self):
        story = stories.SelectOption(self)
        story.toggle_autocomplete()

        expected = self.model.objects.filter(
            owner=self.fixtures.test).values_list('name', flat=True)
        self.assertEqual(sorted(expected),
                         sorted(story.get_suggestions_labels()))
