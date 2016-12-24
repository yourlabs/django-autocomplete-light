from dal import autocomplete

from django import forms

from .models import TModel


class TForm(forms.ModelForm):
    def clean_test(self):
        owner = self.cleaned_data.get('owner', None)
        value = self.cleaned_data.get('test', None)

        if value and owner and value.owner != owner:
            raise forms.ValidationError('Wrong owner for test')

        return value

    class Meta:
        model = TModel
        fields = ('name', 'owner', 'test')
        widgets = {
            'test': autocomplete.ModelSelect2(url='linked_data',
                                              forward=('owner',))
        }

    class Media:
        js = (
            'linked_data.js',
        )
