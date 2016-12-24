from dal import autocomplete

from django import forms

from .models import TModel


class TForm(forms.ModelForm):
    class Meta:
        model = TModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.TaggitSelect2('select2_taggit')
        }
