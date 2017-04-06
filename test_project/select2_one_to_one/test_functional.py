from dal.test import case, stories

from dal_select2.test import Select2Story

from .models import TModel


class AdminOneToOneTestCase(Select2Story, case.AdminMixin, case.OptionMixin,
                            case.AutocompleteTestCase):

    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TModel

    def setUp(self):
        super(AdminOneToOneTestCase, self).setUp()
        self.get(url=self.get_modeladmin_url('add'))

    def test_can_create_option_on_the_fly(self):
        story = stories.CreateOption(self)

        self.enter_text('#id_name', 'special %s' % self.id())

        name = 'new option %s' % self.id()
        story.create_option(name)

        story.assert_value(self.model.objects.get(name=name).pk)
        story.assert_label(name)

        story.submit()

        story.assert_value(self.model.objects.get(name=name).pk)
        story.assert_label(name)
