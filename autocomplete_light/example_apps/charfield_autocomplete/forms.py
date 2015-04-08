import autocomplete_light
from django import forms
from models import Taggable


class TaggableForm(forms.ModelForm):
    class Meta:
        model = Taggable
        widgets = {
            'tags': autocomplete_light.TextWidget('TagAutocomplete'),
        }
