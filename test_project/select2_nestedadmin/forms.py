from dal import autocomplete

from django import forms

from .models import TModelThree


class TFormThree(forms.ModelForm):
    class Meta:
        model = TModelThree
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.ModelSelect2(
                url='nested_linked_data',
                forward=('level_one', 'level_two'),
            )
        }
