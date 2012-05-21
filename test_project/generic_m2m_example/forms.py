import autocomplete_light
from autocomplete_light.contrib.generic_m2m import GenericModelForm, \
    GenericManyToMany

from models import ModelGroup


class ModelGroupForm(GenericModelForm):
    related = GenericManyToMany(
        widget=autocomplete_light.AutocompleteWidget('MyGenericChannel'))

    class Meta:
        model = ModelGroup
