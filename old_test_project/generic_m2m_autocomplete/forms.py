import autocomplete_light
from autocomplete_light.contrib.generic_m2m import GenericModelForm, \
    GenericModelMultipleChoiceField

from models import ModelGroup


class ModelGroupForm(GenericModelForm):
    """
    Use AutocompleteTaggableItems defined in
    gfk_autocomplete.autocomplete_light_registry.
    """

    related = GenericModelMultipleChoiceField(
        widget=autocomplete_light.MultipleChoiceWidget(
            'AutocompleteTaggableItems'))

    class Meta:
        model = ModelGroup
