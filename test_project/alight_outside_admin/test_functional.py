from dal.test import case, stories
from dal_alight.test import AlightStory
from django.urls import reverse

from alight_many_to_many.models import TModel


class AlightOutsideAdminTestCase(
    AlightStory,
    case.OptionMixin,
    case.AutocompleteTestCase,
):
    field_name = 'test'
    model = TModel
    labels_selector = 'autocomplete-select [slot=deck] [data-value]'

    def setUp(self):
        super().setUp()
        self.get(url=reverse('alight_outside_admin'))

    def test_page_loads_with_widget(self):
        assert self.browser.is_element_present_by_css('autocomplete-select')

    def test_can_select_option(self):
        opt = self.create_option()
        story = stories.SelectOptionMultiple(self)
        story.select_option(opt.name)
        labels = [
            self.clean_label(el.text)
            for el in self.browser.find_by_css(self.labels_selector)
        ]
        assert opt.name in labels

    def test_form_submits_with_selection(self):
        opt = self.create_option()
        story = stories.SelectOptionMultiple(self)
        story.select_option(opt.name)
        self.browser.find_by_css('[type=submit]').first.click()
        obj = TModel.objects.first()
        assert obj is not None
