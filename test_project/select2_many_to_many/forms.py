from dal import autocomplete

from django import forms

from .models import TestModel


class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.ModelSelect2Multiple(
                'select2_many_to_many_autocomplete'
            )
        }
