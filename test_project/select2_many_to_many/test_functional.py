from dal.test import case, stories

from dal_select2.test import Select2Story

from .models import TModel


class AdminManyToManyTestCase(Select2Story, case.AdminMixin, case.OptionMixin,
                              case.AutocompleteTestCase):

    field_name = 'test'
    inline_related_name = 'inline_test_models'
    model = TModel

    label_selector = '.select2-selection__choice'

    def setUp(self):
        super(AdminManyToManyTestCase, self).setUp()
        self.get(url=self.get_modeladmin_url('add'))

    def test_can_create_option_on_the_fly_and_select_existing_option(self):
        story = stories.CreateOptionMultiple(self)

        option = self.create_option()
        story.select_option(option.name)

        name = 'new option %s' % self.id()
        story.create_option(name)

        self.enter_text('#id_name', 'special %s' % self.id())
        story.submit()

        story.assert_values((
            self.model.objects.get(name=name).pk,
            option.pk,
        ))
        story.assert_labels((
            name,
            option.name,
        ))
