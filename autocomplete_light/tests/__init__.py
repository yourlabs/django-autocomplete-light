import autocomplete_light
autocomplete_light.autodiscover()

from .forms import (FkModelFormTestCase, OtoModelFormTestCase,
        GfkModelFormTestCase, MtmModelFormTestCase, GmtmModelFormTestCase,
        TaggitModelFormTestCase)

from .fields import ChoiceFieldTestCase, MultipleChoiceFieldTestCase

from .registry import RegistryTestCase
from .templatetags import DataAttributesTestCase
from .views import (RegistryViewTestCase, AutocompleteViewTestCase,
        CreateViewTestCase)

from .exceptions import AutocompleteNotRegisteredTestCase

#from .widget import WidgetTestCase

from .autocomplete.generic import AutocompleteGenericTestCase
from .autocomplete.choice_list import AutocompleteChoiceListTestCase
from .autocomplete.list import AutocompleteListTestCase
from .autocomplete.model import AutocompleteModelTestCase
from .autocomplete.template import AutocompleteModelTemplateTestCase
from .autocomplete.search_fields import (AutocompleteSearchFieldsTestCase,
        AutocompleteGenericSearchFieldsTestCase)
