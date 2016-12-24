from dal import autocomplete

from django import forms

from tagging.forms import TagField

from .models import TModel


class TForm(forms.ModelForm):
    test = TagField(
        widget=autocomplete.TaggingSelect2('select2_tagging'),
        required=False,
    )

    class Meta:
        model = TModel
        exclude = ['for_inline']
