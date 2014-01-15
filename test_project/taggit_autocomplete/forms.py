from django import forms
import autocomplete_light
from autocomplete_light.contrib import taggit_tagfield
from models import TaggitDemo

class TaggitDemoForm(forms.ModelForm):
    tags = taggit_tagfield.TagField(widget=taggit_tagfield.TagWidget('TagAutocomplete'))

    class Meta:
        model = TaggitDemo
