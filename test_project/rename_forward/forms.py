from dal import autocomplete, forward

from django import forms

from .models import TestModel


class TestForm(forms.ModelForm):
    def clean_test(self):
        owner = self.cleaned_data.get('owner', None)
        value = self.cleaned_data.get('test', None)

        if value and owner and value.owner != owner:
            raise forms.ValidationError('Wrong owner for test')

        return value

    class Meta:
        model = TestModel
        fields = ('name', 'owner', 'test')
        widgets = {
            'test': autocomplete.ModelSelect2(
                url='linked_data_rf',
                forward=(forward.Field(src="owner", dst="possessor"),
                         forward.Const(val=42, dst="secret"))
            )
        }

    class Media:
        js = (
            'linked_data.js',
        )
