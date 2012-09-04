"""
Provide tools to enable nice autocompletes in your Django project.
"""
from .registry import AutocompleteRegistry, registry, register, autodiscover
from .autocomplete import *
from .widgets import ChoiceWidget, MultipleChoiceWidget, TextWidget
from .forms import get_widgets_dict, modelform_factory
from .generic import GenericModelForm, GenericModelChoiceField
from .views import CreateView
