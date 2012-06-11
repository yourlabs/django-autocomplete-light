from .base import AutocompleteBase
from .list import AutocompleteList
from .model import AutocompleteModel
from .choice_list import AutocompleteChoiceList
from .template import AutocompleteTemplate
from .generic import AutocompleteGeneric


class AutocompleteListBase(AutocompleteList, AutocompleteBase):
    pass


class AutocompleteChoiceListBase(AutocompleteChoiceList, AutocompleteBase):
    pass


class AutocompleteModelBase(AutocompleteModel, AutocompleteBase):
    pass


class AutocompleteModelTemplate(AutocompleteModel, AutocompleteTemplate):
    pass


class AutocompleteGenericBase(AutocompleteGeneric, AutocompleteBase):
    pass


class AutocompleteGenericTemplate(AutocompleteGeneric, AutocompleteTemplate):
    pass
