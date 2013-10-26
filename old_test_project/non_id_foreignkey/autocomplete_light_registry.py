import autocomplete_light

from .models import CodeModel


class AutocompleteCode(autocomplete_light.AutocompleteModelBase):
    '''Autocomplete for non-id foreign key
    '''
    autocomplete_js_attributes = {'placeholder': u'Start type name...'}
    search_fields = ('name',)

    def choice_value(self, choice):
        return choice.code

    def choices_for_values(self):
        return self.order_choices(self.choices.filter(
            code__in=self.values or []))


autocomplete_light.register(CodeModel, AutocompleteCode)
