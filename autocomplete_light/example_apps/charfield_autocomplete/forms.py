from django import forms

import autocomplete_light

from models import Taggable


class TaggableForm(forms.ModelForm):
    class Meta:
        model = Taggable
        widgets = {
        	'tags': autocomplete_light.TextWidget('TagAutocomplete'),
       	}