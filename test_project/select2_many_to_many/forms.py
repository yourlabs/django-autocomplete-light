from dal import autocomplete

from django import forms

from .models import TestModel


class TestForm(forms.ModelForm):
    test = autocomplete.CreateModelMultipleField(
        required=False,
        queryset=TestModel.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            'select2_many_to_many_autocomplete')
    )

    class Meta:
        model = TestModel
        fields = ('name', 'test')
