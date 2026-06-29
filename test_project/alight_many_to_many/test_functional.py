from dal.test import case
from dal_alight.test import (
    AlightCreateOptionMultiple,
    AlightSelectOptionMultiple,
    AlightStory,
)

from .models import TModel


class AdminManyToManyTestCase(
    AlightStory,
    case.AdminMixin,
    case.OptionMixin,
    case.AutocompleteTestCase,
):
    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TModel
    labels_selector = 'autocomplete-select [slot=deck] [data-value]'

    def setUp(self):
        super().setUp()
        self.get(url=self.get_modeladmin_url('add'))

    def test_can_select_multiple_options(self):
        opt1 = self.create_option()
        opt2 = self.create_option()
        story = AlightSelectOptionMultiple(self)
        story.select_option(opt1.name)
        story.select_option(opt2.name)
        story.assert_selection_persists(
            (opt1.pk, opt2.pk),
            (opt1.name, opt2.name),
        )

    def test_can_create_option_on_the_fly(self):
        story = AlightCreateOptionMultiple(self)
        existing = self.create_option()
        story.select_option(existing.name)

        new_name = 'brand_new_%s' % self.id()
        story.create_option(new_name)

        self.enter_text('#id_name', 'holder_%s' % self.id())
        story.submit()

        created_pk = self.model.objects.get(name=new_name).pk
        story.assert_values((created_pk, existing.pk))
        story.assert_labels((new_name, existing.name))
