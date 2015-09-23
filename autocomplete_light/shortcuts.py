from .autocomplete.shortcuts import *
from .contrib.taggit_field import TaggitField, TaggitWidget
from .exceptions import (AutocompleteArgNotUnderstood,
                         AutocompleteChoicesMustBeQuerySet,
                         AutocompleteLightException, AutocompleteNotRegistered,
                         NoGenericAutocompleteRegistered, NonDjangoModelSubclassException)
from .fields import *
from .forms import *
from .registry import AutocompleteRegistry, autodiscover, register, registry
from .settings import *
from .views import AutocompleteView, CreateView, RegistryView
from .widgets import ChoiceWidget, MultipleChoiceWidget, TextWidget, WidgetBase

try:
    import taggit
except ImportError:
    pass
else:
    from .contrib.taggit_field import TaggitField, TaggitWidget
