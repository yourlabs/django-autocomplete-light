from django import forms

from dal import autocomplete

from .models import TModel


class TForm(forms.ModelForm):
    def clean_test(self):
        group = self.cleaned_data.get('group', None)
        value = self.cleaned_data.get('test', None)

        if value and group and value.group != group:
            raise forms.ValidationError('Wrong group for test')

        return value

    class Meta:
        model = TModel
        fields = ('name', 'group', 'test')
        widgets = {
            'test': autocomplete.ModelAlight(
                url='alight_linked_data',
                forward=('group',),
            )
        }
