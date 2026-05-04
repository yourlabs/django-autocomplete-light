from dal.test import case, stories
from dal.test.utils import OwnedFixtures
from dal_alight.test import AlightStory

from .models import TModel


class AdminSecureDataTest(
    AlightStory,
    case.AdminMixin,
    case.OptionMixin,
    case.AutocompleteTestCase,
):
    field_name = 'test'
    inline_related_name = 'inline_test_models_asd'
    model = TModel

    def setUp(self):
        super().setUp()

        if not getattr(self, 'fixtures', None):
            self.fixtures = OwnedFixtures()
            self.fixtures.install_fixtures(self.model)

        self.get(url=self.get_modeladmin_url('add'))

    def test_filtered_options(self):
        story = stories.SelectOption(self)
        story.toggle_autocomplete()

        story.assert_suggestion_labels_are(
            self.model.objects.filter(
                owner=self.fixtures.test
            ).values_list('name', flat=True)
        )
