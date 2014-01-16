"""Support for django-taggit tags system using the
MultipleChoiceWidget. A django-taggit field will default to a
TextWidget. To enable use of the MultipleChoiceWidget, this class must
be registered explicitly. eg:

from autocomplete_light import AutocompleteTaggitMultipleChoice
autocomplete_light.register(Tag, AutocompleteMultipleChoiceTag)

Tags must be created before they can be selected. Hence if you want
tags to be dynamically created then use the default interface.


.. Warning::
    In this case, the tags field is a relation. Thus form.save() **must** be
    called with commit=True.

.. Warning:: 
    Tags that are created after the form has been loaded are
    selectable, but will be marked as invalid when the form is
    saved. After tags are added the form must be reloaded.

"""

from django.utils.encoding import force_text
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _, ungettext_lazy
from .choice_list import AutocompleteChoiceList
from .base import AutocompleteBase
from .model import AutocompleteModel

try:
    from taggit.utils import parse_tags

except ImportError:
    parse_tags = None

__all__ = ('AutocompleteTaggitChoiceList',)

class AutocompleteTaggitChoiceList(AutocompleteChoiceList, AutocompleteBase, AutocompleteModel):
    search_fields = ('name',)
    order_by = lambda cls, choice: unicode(choice).lower()
    autocomplete_js_attributes={'placeholder': 'Enter tag...',}
    error_messages = {
        'invalid_data_type': _('Function %(function)s does not support this data type: %(type)s'),
    }
    choices = None

    def __init__(self, request=None, values=None, *args, **kwargs):
        super(AutocompleteTaggitChoiceList, self).__init__(*args, **kwargs)
        self.request = request
        self.values = values if values is not None else []

    def _set_values(self, values):
        choices = self.choices.all()
        self._values = [] 
        for val in values:
            if val != None:
                self._values.append(self.format_value(val, choices))
                
    def _get_values(self):
        return self._values
        
    values = property(_get_values, _set_values)

    def format_value(self, value, choices = None):
        if choices == None:
            choices = self.choices.all()
        if isinstance(value, basestring):
            return value
        if isinstance(value, int):
            for choice in choices:
                if choice.id == value:
                    return choice.name
        if hasattr(value, 'tag'):
            return value.tag.name
        raise ValidationError(self.error_messages['invalid_data_type'],
                              code = 'invalid_data_type',
                              params = {'function' : 'AutocompleteTaggitChoiceList.format_value',
                                        'type' : str(type(value)), } 
            )
            

    def choices_for_values(self):
        values_choices = []
        return self.order_choices(self.choices.filter(
            name__in=self.values or []))

        
    def choices_for_request(self):
        assert self.choices is not None, 'choices should be a queryset'
        assert self.search_fields, 'autocomplete.search_fields must be set'

        q = self.request.GET.get('q', '').strip()

        conditions = self._choices_for_request_conditions(q, self.search_fields)
        
        request_choices = self.choices.filter(conditions)
        return self.order_choices(request_choices)[0:self.limit_choices]

    def choice_value(self, choice):
        return choice.name

    def choice_label(self, choice):
        return unicode(choice)
