from django.utils import simplejson
from django import forms
from django.forms.util import flatatt
from django.utils import safestring
from django.template.loader import render_to_string

from .channel import *

__all__ = ['AutocompleteWidget']

class AutocompleteWidget(forms.SelectMultiple):
    """
    Widget suitable for ModelChoiceField and ModelMultipleChoiceField.

    Example usage::

        from django import forms

        import autocomplete_light

        from models import Author

        class AuthorsForm(forms.Form):
            lead_author = forms.ModelChoiceField(Author.objects.all(), widget=
                autocomplete_light.AutocompleteWidget('AuthorChannel', max_items=1))
            contributors = forms.ModelMultipleChoiceField(Author.objects.all(), widget=
                autocomplete_light.AutocompleteWidget('AuthorChannel'))
    """

    class Media:
        js = ('autocomplete_light/autocomplete.js',)

    def __init__(self, channel_name, *args, **kwargs):
        """
        Decorates SelectMultiple constructor 

        Arguments:
        channel_name -- the name of the channel that this widget should use.

        Keyword arguments are passed to javascript via data attributes of the
        autocomplete wrapper element:

        max_items
            The number of items that this autocomplete allows. If set to 0,
            then it allows any number of selected items like a multiple select,
            well suited for ManyToMany relations or any kind of
            ModelMultipleChoiceField. If set to 3 for example, then it will
            only allow 3 selected items. It should be set to 1 if the widget is
            for a ModelChoiceField or ForeignKey, in that case it would be like
            a normal select. Default is 0.
        
        min_characters
            The minimum number of characters before the autocomplete box shows
            up. If set to 2 for example, then the autocomplete box will show up
            when the input receives the second character, for example 'ae'. If
            set to 0, then the autocomplete box will show up as soon as the
            input is focused, even if it's empty, behaving like a normal
            select. Default is 0.

        bootstrap
            The name of the bootstrap kind. By default, deck.js will only
            initialize decks for wrappers that have data-bootstrap="normal". If
            you want to implement your own bootstrapping logic in javascript,
            then you set bootstrap to anything that is not "normal". By
            default, its value is copied from channel.bootstrap.
        """
        self.channel_name = channel_name
        
        from autocomplete_light import registry
        self.channel = registry[channel_name]()

        self.max_items = kwargs.pop('max_items', 0)
        self.min_characters = kwargs.pop('min_characters', 0)
        self.bootstrap = kwargs.pop('bootstrap', self.channel.bootstrap)

        super(AutocompleteWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        """
        Render the autocomplete widget.

        It will try two templates, like django admin:
        - autocomplete_light/channelname/widget.html
        - autocomplete_light/widget.html

        Note that it will not pass 'value' to the template, because 'value'
        might be a list of model ids in the case of ModelMultipleChoiceField,
        or a model id in the case of ModelChoiceField. To keep things simple,
        it will just pass a list, 'values', to the template context.
        """
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
        """Route to Select if max_items is 1, else route to SelectMultiple"""
        if self.max_items == 1:
            return forms.Select.value_from_datadict(self, data, files, name)
        else:
            return forms.SelectMultiple.value_from_datadict(self, data, files, name)

    def _has_changed(self, initial, data):
        """Route to Select if max_items is 1, else route to SelectMultiple"""
        if self.max_items == 1:
            return forms.Select._has_changed(self, initial, data)
        else:
            return forms.SelectMultiple._has_changed(self, initial, data)
