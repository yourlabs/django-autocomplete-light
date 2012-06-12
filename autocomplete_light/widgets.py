from django import forms
from django.forms.util import flatatt
from django.utils import safestring
from django.template.loader import render_to_string

__all__ = ['ChoiceWidget', 'MultipleChoiceWidget']


class WidgetBase(object):
    """
    Widget suitable for ModelChoiceField and ModelMultipleChoiceField.
    """

    def __init__(self, autocomplete_name=None, autocomplete=None,
        widget_js_attributes={}, autocomplete_js_attributes={}):

        assert autocomplete_name or autocomplete, \
            'widget needs autocomplete_name or autocomplete'

        if autocomplete_name is not None:
            self.autocomplete_name = autocomplete_name
            from autocomplete_light import registry
            self.autocomplete = registry[autocomplete_name]
        elif autocomplete is not None:
            self.autocomplete = autocomplete
            self.autocomplete_name = autocomplete.__class__.__name__

        self.widget_js_attributes = widget_js_attributes
        self.autocomplete_js_attributes = autocomplete_js_attributes

    def process_js_attributes(self):
        more_autocomplete_js_attributes = getattr(self.autocomplete,
            'autocomplete_js_attributes', {})
        self.autocomplete_js_attributes.update(
            more_autocomplete_js_attributes)

        more_widget_js_attributes = getattr(self.autocomplete,
            'widget_js_attributes', {})
        self.widget_js_attributes.update(
            more_widget_js_attributes)

        if 'bootstrap' not in self.widget_js_attributes.keys():
            self.widget_js_attributes['bootstrap'] = 'normal'

        if 'choice_selector' not in self.autocomplete_js_attributes.keys():
            self.autocomplete_js_attributes['choice_selector'] = '[data-value]'

        if 'url' not in self.autocomplete_js_attributes.keys():
            url = self.autocomplete().get_absolute_url()
            self.autocomplete_js_attributes['url'] = url

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
            }
        ))

    def as_dict(self):
        return {
            'max_values': self.max_values,
            'min_characters': self.min_characters,
            'bootstrap': self.bootstrap,
            # cast to unicode as it might be a gettext proxy
            'placeholder': unicode(self.placeholder),
        }


class ChoiceWidget(WidgetBase, forms.Select):
    def __init__(self, autocomplete_name=None, autocomplete=None,
       widget_js_attributes={}, autocomplete_js_attributes={},
       *args, **kwargs):

        forms.Select.__init__(self, *args, **kwargs)

        WidgetBase.__init__(self, autocomplete_name, autocomplete,
            widget_js_attributes, autocomplete_js_attributes)

        self.widget_js_attributes['max_values'] = 1


class MultipleChoiceWidget(WidgetBase, forms.SelectMultiple):
    def __init__(self, autocomplete_name=None, autocomplete=None,
       widget_js_attributes={}, autocomplete_js_attributes={},
       *args, **kwargs):

        forms.SelectMultiple.__init__(self, *args, **kwargs)

        WidgetBase.__init__(self, autocomplete_name, autocomplete,
            widget_js_attributes, autocomplete_js_attributes)
