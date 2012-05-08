from django.utils import simplejson
from django import forms
from django.forms.util import flatatt
from django.utils import safestring
from django.template.loader import render_to_string

from .channel import *

__all__ = ['AutocompleteWidget']

class AutocompleteWidget(forms.SelectMultiple):
    class Media:
        js = (
            'autocomplete_light/autocomplete.js',
            'autocomplete_light/deck.js',
        )

    def __init__(self, channel_name, *args, **kwargs):
        self.channel_name = channel_name
        
        from autocomplete_light import registry
        self.channel = registry[channel_name]()
        
        self.max_items = kwargs.pop('max_items', 0)
        self.min_characters = kwargs.pop('min_characters', 0)

        super(AutocompleteWidget, self).__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)

        if value and not isinstance(value, (list, tuple)):
            values = [value]
        else:
            values = value
       
        if values and not self.channel.are_valid(values):
            raise forms.ValidationError('%s cannot find pk(s) %s' % (self.channel_name, values))
       
        return safestring.mark_safe(render_to_string([
                'autocomplete_light/%s/widget.html' % self.channel_name.lower(),
                'autocomplete_light/widget.html',
            ], {
                'widget': self,
                'name': name,
                'values': values,
                'channel': self.channel,
                'results': self.channel.get_results(values or []),
                'json_value': safestring.mark_safe(simplejson.dumps(value)),
                'json_channel': safestring.mark_safe(simplejson.dumps(
                    self.channel.as_dict())),
                'extra_attrs': safestring.mark_safe(flatatt(final_attrs)),
            }
        ))
    
    # we might want to split up in two widgets for that ... is it necessary ?
    # apparently not yet, but maybe at next django release
    def value_from_datadict(self, data, files, name):
        if self.max_items == 1:
            return forms.Select.value_from_datadict(self, data, files, name)
        else:
            return forms.SelectMultiple.value_from_datadict(self, data, files, name)

    def _has_changed(self, initial, data):
        if self.max_items == 1:
            return forms.Select._has_changed(self, initial, data)
        else:
            return forms.SelectMultiple._has_changed(self, initial, data)


