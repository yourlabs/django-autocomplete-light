from dal import autocomplete, forward

from django import forms

from .models import TModel


class TForm(forms.ModelForm):
    checkbox = forms.BooleanField(label='checkbox',
                                  required=False,
                                  initial=False)

    class Meta:
        model = TModel
        fields = ('name', 'checkbox', 'owner', 'test')
        widgets = {
            'test': autocomplete.ModelSelect2(
                url='linked_data_rf',
                forward=(forward.Field(src="checkbox"),
                         forward.Field(src="owner", dst="possessor"),
                         forward.Const(val=42, dst="secret"))
            )
        }

    class Media:
        js = (
            'linked_data.js',
        )
