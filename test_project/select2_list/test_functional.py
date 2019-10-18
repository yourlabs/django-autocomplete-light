import uuid

from dal.test import case, stories

from dal_select2.test import Select2Story

import six

from .models import TModel


def random_text():
    return six.text_type(uuid.uuid1())


class AdminSelect2List(Select2Story, case.AdminMixin, case.OptionMixin,
                       case.AutocompleteTestCase):
    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TModel

    def create_option(self):
        """Return option, content type."""
        option = super(AdminSelect2List, self).create_option()
        option.test = random_text()
        option.save()

        return option

    def setUp(self):
        super(AdminSelect2List, self).setUp()
        self.get(url=self.get_modeladmin_url('add'))
        self.fill_name()

    def test_can_select_option(self):
        option = self.create_option()
        story = stories.SelectOption(self)
        story.select_option(option.test)
        story.assert_selection_persists(option.test, option.test)

    def test_can_select_option_in_first_inline(self):
        option = self.create_option()
        story = stories.InlineSelectOption(self, inline_number=0)
        story.select_option(option.test)
        story.assert_selection(option.test, option.test)

    def test_can_select_option_in_first_extra_inline(self):
        option = self.create_option()
        story = stories.InlineSelectOption(self, inline_number=3)
        story.select_option(option.test)
        story.assert_selection(option.test, option.test)

    def test_can_change_selected_option(self):
        option = self.create_option()
        story = stories.SelectOption(self)
        story.select_option(option.test)
        story.assert_selection_persists(option.test, option.test)
        option = self.create_option()
        story.select_option(option.test)
        story.assert_selection_persists(option.test, option.test)

    def test_can_create_new_option(self):
        new_option_text = random_text()
        story = stories.CreateOption(self, new_option_text)
        story.select_option(new_option_text)
        story.assert_selection(new_option_text, new_option_text)
