from django import forms

from dal import autocomplete

from .models import TModel


class TForm(forms.ModelForm):
    class Meta:
        model = TModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.ModelAlight(url='alight_secure_data_autocomplete')
        }
