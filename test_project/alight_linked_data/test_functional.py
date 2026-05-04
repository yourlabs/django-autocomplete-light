from dal.test import case, stories
from dal_alight.test import AlightStory

from .models import Group, TModel


class AdminLinkedDataTestCase(
    AlightStory,
    case.AdminMixin,
    case.OptionMixin,
    case.AutocompleteTestCase,
):
    field_name = 'test'
    inline_related_name = 'related_test_models'
    model = TModel

    def setUp(self):
        super().setUp()
        self.group_a = Group.objects.create(name='GroupA')
        self.group_b = Group.objects.create(name='GroupB')
        self.item_a = TModel.objects.create(name='item_a', group=self.group_a)
        self.item_b = TModel.objects.create(name='item_b', group=self.group_b)
        self.get(url=self.get_modeladmin_url('add'))

    def _set_group(self, group_pk):
        self.browser.execute_script(
            'document.querySelector("[name=group]").value = %s' % group_pk
        )

    def test_options_filter_by_forward_field(self):
        story = stories.SelectOption(self)
        story.toggle_autocomplete()
        story.assert_suggestion_labels_are(
            TModel.objects.values_list('name', flat=True)
        )

        self._set_group(self.group_a.pk)
        story.refresh_autocomplete()
        story.assert_suggestion_labels_are(['item_a'])

        self._set_group(self.group_b.pk)
        story.refresh_autocomplete()
        story.assert_suggestion_labels_are(['item_b'])

    def test_can_select_filtered_option(self):
        self._set_group(self.group_a.pk)
        story = stories.SelectOption(self)
        story.select_option(self.item_a.name)
        story.assert_selection_persists(self.item_a.pk, self.item_a.name)
