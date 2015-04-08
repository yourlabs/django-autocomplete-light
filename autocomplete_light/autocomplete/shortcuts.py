from .base import AutocompleteBase
from .choice_list import AutocompleteChoiceList
from .generic import AutocompleteGeneric
from .list import AutocompleteList
from .model import AutocompleteModel
from .rest_model import AutocompleteRestModel
from .template import AutocompleteTemplate


class AutocompleteListBase(AutocompleteList, AutocompleteBase):
    """
    Use :py:class:`~base.AutocompleteBase` for rendering logic and
    :py:class:`~list.AutocompleteList` for business logic.
    """
    pass


class AutocompleteListTemplate(AutocompleteList, AutocompleteTemplate):
    """
    Use :py:class:`~template.AutocompleteTemplate` for rendering logic and
    :py:class:`~list.AutocompleteList` for business logic.
    """
    pass


class AutocompleteChoiceListBase(AutocompleteChoiceList, AutocompleteBase):
    """
    Use :py:class:`~base.AutocompleteBase` for rendering logic and
    :py:class:`~choice_list.AutocompleteChoiceList` for
    business logic.
    """
    pass


class AutocompleteChoiceListTemplate(AutocompleteChoiceList,
        AutocompleteTemplate):
    """
    Use :py:class:`~template.AutocompleteTemplate` for rendering logic and
    :py:class:`~choice_list.AutocompleteChoiceList` for business logic.
    """
    pass


class AutocompleteModelBase(AutocompleteModel, AutocompleteBase):
    """
    Use :py:class:`~base.AutocompleteBase` for rendering logic and
    :py:class:`~model.AutocompleteModel` for business logic.
    """
    pass


class AutocompleteModelTemplate(AutocompleteModel, AutocompleteTemplate):
    """
    Use :py:class:`~template.AutocompleteTemplate` for rendering logic and
    :py:class:`~model.AutocompleteModel` for business logic.

    It also sets a default :py:attr:`choice_template`.
    """
    choice_template = 'autocomplete_light/model_template/choice.html'


class AutocompleteGenericBase(AutocompleteGeneric, AutocompleteBase):
    """
    Use :py:class:`~base.AutocompleteBase` for rendering logic and
    :py:class:`~generic.AutocompleteGeneric` for business logic.
    """
    pass


class AutocompleteGenericTemplate(AutocompleteGeneric, AutocompleteTemplate):
    """
    Use :py:class:`~template.AutocompleteTemplate` for rendering logic and
    :py:class:`~generic.AutocompleteGeneric` for business logic.
    """
    pass


class AutocompleteRestModelBase(AutocompleteRestModel, AutocompleteBase):
    """
    Use :py:class:`~base.AutocompleteBase` for rendering logic and
    :py:class:`~rest_model.AutocompleteRestModel` for business logic.
    """
    pass


class AutocompleteRestModelTemplate(AutocompleteRestModel,
                                    AutocompleteTemplate):
    """
    Use :py:class:`~template.AutocompleteTemplate` for rendering logic and
    :py:class:`~rest_model.AutocompleteRestModel` for business logic.
    """
    pass
