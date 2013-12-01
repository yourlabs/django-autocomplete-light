"""
Provide tools to enable nice autocompletes in your Django project.
"""
from .registry import AutocompleteRegistry, registry, register, autodiscover

from .autocomplete import *

from .widgets import ChoiceWidget, MultipleChoiceWidget, TextWidget

from .forms import *

from .fields import *

from .views import CreateView
from .exceptions import AutocompleteNotRegistered

from .settings import *
