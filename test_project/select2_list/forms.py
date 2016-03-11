from dal import autocomplete

from django import forms

from .models import TestModel


class TestForm(forms.ModelForm):
    test = forms.ChoiceField(
        choices=[
            ('windows', 'windows'),
            ('linux', 'linux'),
        ],
        required=False,
        widget=autocomplete.Select2(url='select2_list')
    )

    class Meta:
        model = TestModel
        fields = ('name', 'test')
