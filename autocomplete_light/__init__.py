"""
Provide tools to enable nice autocompletes in your Django project.
"""
from .registry import ChannelRegistry, registry, register, autodiscover, static_list
from .channel import ChannelBase, JSONChannelBase
from .widgets import AutocompleteWidget
from .forms import get_widgets_dict, modelform_factory
