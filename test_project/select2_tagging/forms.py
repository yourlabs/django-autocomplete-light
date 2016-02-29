from dal import autocomplete

from django import forms

from tagging.forms import TagField

from .models import TestModel


class TestForm(forms.ModelForm):
    test = TagField(widget=autocomplete.TaggingSelect2('select2_tagging'))

    class Meta:
        model = TestModel
        exclude = ['for_inline']
