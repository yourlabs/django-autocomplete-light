import autocomplete_light
autocomplete_light.autodiscover()

from .forms import (
    SelectMultipleHelpTextRemovalMixinTestCase,
    SelectMultipleHelpTextRemovalMixinFrTestCase,
    FkModelFormTestCase,
    OtoModelFormTestCase,
    GfkModelFormTestCase,
    MtmModelFormTestCase,
    GmtmModelFormTestCase,
    TaggitModelFormTestCase,
    TestUnuseableVirtualfield
)

from .fields import ChoiceFieldTestCase, MultipleChoiceFieldTestCase

from .registry import (
    RegistryTestCase,
    RegistryGetAutocompleteFromArgTestCase,
    AppConfigSupportTestCase,
)

from .templatetags import DataAttributesTestCase
from .views import (RegistryViewTestCase, AutocompleteViewTestCase,
        CreateViewTestCase)

from .exceptions import AutocompleteNotRegisteredTestCase

from .widget import (
    ActivateAutocompleteInBlankFormTestCase,
    SelectChoiceInEmptyFormTestCase,
    WidgetInitialStatusInEditForm,
    RemoveChoiceInEditFormTestCase,
    XhrPendingTestCase,
    KeyboardTestCase,
    InlineBlankTestCase,
    InlineSelectChoiceTestCase,
)

from .widgets import (
    ChoiceWidgetTestCase,
    MultipleChoiceWidgetTestCase,
    TextWidgetTestCase,
)

from .fields import (
    ChoiceFieldTestCase,
    MultipleChoiceFieldTestCase,
    ModelChoiceFieldTestCase,
    ModelMultipleChoiceFieldTestCase,
    GenericModelChoiceFieldTestCase,
    GenericModelMultipleChoiceFieldTestCase
)

from .dependent import (
    DependentAutocompleteEmptyFormTestCase,
)

from .autocomplete.generic import AutocompleteGenericTestCase
from .autocomplete.choice_list import AutocompleteChoiceListTestCase
from .autocomplete.list import AutocompleteListTestCase
from .autocomplete.model import AutocompleteModelTestCase
from .autocomplete.template import AutocompleteModelTemplateTestCase
from .autocomplete.search_fields import (AutocompleteSearchFieldsTestCase,
        AutocompleteGenericSearchFieldsTestCase)
from .autocomplete.get_add_another_url import GetAddAnotherUrlTestCase
