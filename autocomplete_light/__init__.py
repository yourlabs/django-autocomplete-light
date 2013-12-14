"""
Provide tools to enable nice autocompletes in your Django project.
"""
from .registry import AutocompleteRegistry, registry, register, autodiscover

from .autocomplete import *

from .widgets import WidgetBase, ChoiceWidget, MultipleChoiceWidget, TextWidget

from .forms import *

from .fields import *

try:
    import taggit
except ImportError:
    pass
else:
    from .contrib.taggit_field import TaggitField, TaggitWidget

from .views import CreateView, RegistryView, AutocompleteView
from .exceptions import AutocompleteNotRegistered

from .settings import *
