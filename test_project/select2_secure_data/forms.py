from django import forms

from dal import autocomplete

from .models import TModel


class TForm(forms.ModelForm):
    class Meta:
        model = TModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.ModelSelect2(url='secure_data')
        }
