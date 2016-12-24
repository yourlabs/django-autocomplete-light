from dal import autocomplete

from django import forms

from .models import TModel


class TForm(forms.ModelForm):
    class Meta:
        model = TModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.ModelSelect2Multiple(
                'select2_many_to_many_autocomplete'
            )
        }
