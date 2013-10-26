from django import forms

import autocomplete_light

from models import OptionnalTaggedItem


class OptionnalTaggedItemForm(autocomplete_light.GenericModelForm):
    """
    Use AutocompleteTaggableItems defined in
    gfk_autocomplete.autocomplete_light_registry.
    """
    content_object = autocomplete_light.GenericModelChoiceField(
        required=False, widget=autocomplete_light.ChoiceWidget(
            autocomplete='AutocompleteTaggableItems'))

    class Meta:
        model = OptionnalTaggedItem
        exclude = ('content_type', 'object_id')
