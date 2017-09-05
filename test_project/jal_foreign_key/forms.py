from dal import autocomplete

from django import forms

from .models import TModel


class TestForm(forms.ModelForm):
    class Meta:
        model = TModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.JalChoiceWidget(url='jal_fk')
        }
