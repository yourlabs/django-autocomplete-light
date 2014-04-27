"""
Provide tools to enable nice autocompletes in your Django project.
"""
from .registry import AutocompleteRegistry, registry, register, autodiscover

from .autocomplete import *

from .widgets import WidgetBase, ChoiceWidget, MultipleChoiceWidget, TextWidget

from .contrib.taggit_field import TaggitWidget, TaggitField

from .forms import *

from .fields import *

try:
    import taggit
except ImportError:
    pass
else:
    from .contrib.taggit_field import TaggitField, TaggitWidget

from .views import CreateView, RegistryView, AutocompleteView
from .exceptions import (AutocompleteNotRegistered,
                         NoGenericAutocompleteRegistered,
                         AutocompleteArgNotUnderstood,
                         AutocompleteLightException)

from .settings import *

default_app_config = 'autocomplete_light.apps.AutocompleteLightConfig'
