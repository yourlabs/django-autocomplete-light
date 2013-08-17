import os

import autocomplete_light
autocomplete_light.autodiscover()

from .registry import RegistryTestCase
from .templatetags import DataAttributesTestCase
from .generic import GenericModelFormTestCase
from .generic_m2m import AutocompleteGenericM2MTestCase
from .exceptions import AutocompleteNotRegisteredTestCase

"""
Selenium tests (which have waits and all) don't work on travis since the
update, i don't know why, i've spent countless hours trying to debug it, asked
numerous times on #travis, was recommended to contact support which i did
but support didn't reply so here goes ....
"""
if not os.environ.get('TRAVIS', False):
    from .widget import WidgetTestCase

from .autocomplete.choice_list import AutocompleteChoiceListTestCase
from .autocomplete.list import AutocompleteListTestCase
from .autocomplete.model import AutocompleteModelTestCase
from .autocomplete.template import AutocompleteModelTemplateTestCase
from .autocomplete.generic import AutocompleteGenericTestCase
from .autocomplete.search_fields import AutocompleteSearchFieldsTestCase
