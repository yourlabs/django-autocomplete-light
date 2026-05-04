from django import forms

from dal import autocomplete

from .models import TModel


class TForm(forms.ModelForm):
    test = autocomplete.AlightListCreateChoiceField(
        choice_list=['apple', 'apricot', 'banana', 'cherry'],
        widget=autocomplete.ListAlight(url='alight_list'),
        required=False,
    )

    class Meta:
        model = TModel
        fields = ('test',)
