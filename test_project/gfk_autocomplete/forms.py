from django import forms

import autocomplete_light

from models import TaggedItem


class TaggedItemForm(autocomplete_light.GenericModelForm):
    content_object = autocomplete_light.GenericModelChoiceField(
        widget=autocomplete_light.ChoiceWidget(
            autocomplete_name='AutocompleteTaggableItems'))

    class Meta:
        model = TaggedItem
        exclude = ('content_type', 'object_id')
