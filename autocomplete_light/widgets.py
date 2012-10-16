"""
ChoiceWidget is intended to work as a replacement for django's Select widget,
and MultipleChoiceWidget for django's SelectMultiple.

Constructing a widget needs an Autocomplete class or registered autocomplete
name.

The choice autocomplete widget renders from autocomplete_light/widget.html
template.
"""

from django import forms
from django.forms.util import flatatt
from django.utils import safestring
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

__all__ = ['ChoiceWidget', 'MultipleChoiceWidget']


class WidgetBase(object):
    """
    Base widget for autocompletes.

    Mainly handles passing arguments from Python to HTML data-* attributes,
    via widget_js_attributes and autocomplete_js_attributes. Javascript will
    parse these data-* attributes.

    This widget also renders the widget template.
    """

    def __init__(self, autocomplete,
                 widget_js_attributes=None, autocomplete_js_attributes=None,
                 add_another_url=None):

        if isinstance(autocomplete, basestring):
            self.autocomplete_name = autocomplete
            from autocomplete_light import registry
            self.autocomplete = registry[self.autocomplete_name]
        else:
            self.autocomplete = autocomplete
            self.autocomplete_name = autocomplete.__class__.__name__

        if widget_js_attributes is None:
            self.widget_js_attributes = {}
        else:
            self.widget_js_attributes = widget_js_attributes

        if autocomplete_js_attributes is None:
            self.autocomplete_js_attributes = {}
        else:
            self.autocomplete_js_attributes = autocomplete_js_attributes

        self.add_another_url = add_another_url

    def process_js_attributes(self):
        extra_autocomplete_js_attributes = getattr(self.autocomplete,
            'autocomplete_js_attributes', {})
        self.autocomplete_js_attributes.update(
            extra_autocomplete_js_attributes)

        extra_widget_js_attributes = getattr(self.autocomplete,
            'widget_js_attributes', {})
        self.widget_js_attributes.update(
            extra_widget_js_attributes)

        if 'bootstrap' not in self.widget_js_attributes.keys():
            self.widget_js_attributes['bootstrap'] = 'normal'

        if 'choice_selector' not in self.autocomplete_js_attributes.keys():
            self.autocomplete_js_attributes['choice_selector'] = '[data-value]'

        if 'url' not in self.autocomplete_js_attributes.keys():
            url = self.autocomplete().get_absolute_url()
            self.autocomplete_js_attributes['url'] = url

        if 'placeholder' not in self.autocomplete_js_attributes.keys():
            self.autocomplete_js_attributes['placeholder'] = _(
                'type some text to search in this autocomplete').capitalize()

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)

        if value and not isinstance(value, (list, tuple)):
            values = [value]
        else:
            values = value

        autocomplete = self.autocomplete(values=values)

        if values and not autocomplete.validate_values():
            raise forms.ValidationError('%s cannot validate %s' % (
                self.autocomplete_name, values))

        self.process_js_attributes()

        autocomplete_name = self.autocomplete_name.lower()
        return safestring.mark_safe(render_to_string([
            'autocomplete_light/%s/widget.html' % autocomplete_name,
            'autocomplete_light/widget.html',
        ], {
            'name': name,
            'values': values,
            'widget': self,
            'extra_attrs': safestring.mark_safe(flatatt(final_attrs)),
            'autocomplete': autocomplete,
        }))


class ChoiceWidget(WidgetBase, forms.Select):
    """
    Widget that provides an autocomplete for zero to one choice.
    """

    def __init__(self, autocomplete,
                 widget_js_attributes=None, autocomplete_js_attributes=None,
                 *args, **kwargs):

        forms.Select.__init__(self, *args, **kwargs)

        WidgetBase.__init__(self, autocomplete,
            widget_js_attributes, autocomplete_js_attributes)

        self.widget_js_attributes['max_values'] = 1


class MultipleChoiceWidget(WidgetBase, forms.SelectMultiple):
    """
    Widget that provides an autocomplete for zero to n choices.
    """
    def __init__(self, autocomplete=None,
                 widget_js_attributes=None, autocomplete_js_attributes=None,
                 *args, **kwargs):

        forms.SelectMultiple.__init__(self, *args, **kwargs)

        WidgetBase.__init__(self, autocomplete,
            widget_js_attributes, autocomplete_js_attributes)


class TextWidget(forms.TextInput, WidgetBase):
    def __init__(self, autocomplete,
                 widget_js_attributes=None, autocomplete_js_attributes=None,
                 *args, **kwargs):

        forms.TextInput.__init__(self, *args, **kwargs)

        WidgetBase.__init__(self, autocomplete,
            widget_js_attributes, autocomplete_js_attributes)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = forms.TextInput.build_attrs(self, extra_attrs, **kwargs)

        def update_attrs(source, prefix=''):
            for key, value in source.items():
                key = u'data-%s%s' % (prefix, key.replace('_', '-'))
                attrs[key] = value

        self.process_js_attributes()
        update_attrs(self.widget_js_attributes)
        update_attrs(self.autocomplete_js_attributes, 'autocomplete-')

        if 'class' not in attrs.keys():
            attrs['class'] = ''
        attrs['class'] += 'autocomplete-light-text-widget'

        return attrs
