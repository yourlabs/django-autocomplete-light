from .base import AutocompleteBase
from .list import AutocompleteList
from .model import AutocompleteModel
from .choice_list import AutocompleteChoiceList
from .template import AutocompleteTemplate
from .generic import AutocompleteGeneric
from .proxy import AutocompleteProxyInterface, AutocompleteProxy
from .model_proxy import AutocompleteModelProxy


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


class AutocompleteProxyBase(AutocompleteProxy, AutocompleteBase):
    choice_html_format = ''.join([
        u'<div data-value="%s">%s',
        u'<textarea style="display:none">%s</textarea>',
        u'</div>',
    ])

    def choice_html(self, choice):
        """
        Return a choice formated according to self.choice_html_format.
        """
        return self.choice_html_format % (
            self.choice_value(choice), self.choice_label(choice),
            self.choice_serialize(choice))


class AutocompleteModelProxyBase(AutocompleteModel, AutocompleteModelProxy,
    AutocompleteProxyBase):
    pass
