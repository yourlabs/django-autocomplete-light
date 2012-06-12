"""
Provide tools to enable nice autocompletes in your Django project.
"""
from .registry import AutocompleteRegistry, registry, register, autodiscover
from .autocomplete import AutocompleteBase, \
    AutocompleteList, AutocompleteListBase, \
    AutocompleteChoiceList, AutocompleteChoiceListBase, \
    AutocompleteModel, AutocompleteModelBase, \
    AutocompleteTemplate, AutocompleteModelTemplate, \
    AutocompleteGeneric, AutocompleteGenericBase, AutocompleteGenericTemplate
from .widgets import ChoiceWidget, MultipleChoiceWidget
from .forms import get_widgets_dict, modelform_factory
from .generic import GenericModelForm, GenericModelChoiceField
