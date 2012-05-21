"""
Provide tools to enable nice autocompletes in your Django project.
"""
from .registry import ChannelRegistry, registry, register, autodiscover
from .channel import ChannelBase, JSONChannelBase, RemoteChannelBase, \
    GenericChannelBase
from .widgets import AutocompleteWidget
from .forms import get_widgets_dict, modelform_factory
from .generic import GenericModelForm, GenericForeignKeyField
