import autocomplete_light
autocomplete_light.autodiscover()

from .registry import RegistryTestCase
from .templatetags import DataAttributesTestCase
from .generic import GenericModelFormTestCase
from .generic_m2m import AutocompleteGenericM2MTestCase
from .exceptions import AutocompleteNotRegisteredTestCase
from .widget import WidgetTestCase

from .autocomplete.choice_list import AutocompleteChoiceListTestCase
from .autocomplete.list import AutocompleteListTestCase
from .autocomplete.model import AutocompleteModelTestCase
from .autocomplete.template import AutocompleteModelTemplateTestCase
from .autocomplete.generic import AutocompleteGenericTestCase
from .autocomplete.search_fields import (AutocompleteSearchFieldsTestCase,
        AutocompleteGenericSearchFieldsTestCase)
