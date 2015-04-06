from .widgets import WidgetBase, ChoiceWidget, MultipleChoiceWidget, TextWidget

from .autocomplete.shortcuts import *
    
from .contrib.taggit_field import TaggitWidget, TaggitField

from .forms import *

from .fields import *

try:
    import taggit
except ImportError:
    pass
else:
    from .contrib.taggit_field import TaggitField, TaggitWidget

from .registry import registry, AutocompleteRegistry, autodiscover, register
from .views import CreateView, RegistryView, AutocompleteView
from .exceptions import (AutocompleteNotRegistered,
                         NoGenericAutocompleteRegistered,
                         AutocompleteArgNotUnderstood,
                         AutocompleteLightException)

from .settings import *
