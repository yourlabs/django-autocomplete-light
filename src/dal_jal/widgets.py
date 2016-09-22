# -*- coding: utf-8 -*-
"""jquery-autocomplete-light widget implementation module."""
from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.utils import safestring
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt

from dal.widgets import WidgetMixin


__all__ = ['JalWidgetMixin', 'JalChoiceWidget', 'JalMultipleChoiceWidget', 'JalTextWidget']


class JalWidgetMixin(object):
    class Media:
        """Automatically include static files for form.media."""
        css = {
            'all': (
                'autocomplete_light/vendor/jal/src/style.css',
            ),
        }
        js = (
            'autocomplete_light/jquery.init.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/vendor/jal/src/autocomplete.js',
            'autocomplete_light/vendor/jal/src/widget.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/jal.js',
        )

    autocomplete_function = 'jal'

    @property
    def view(self):
        view_func = resolve(self.url).func
        module = importlib.import_module(view_func.__module__)
        return getattr(module, view_func.__name__)

    def render(self, name, value, attrs=None):
        html = '''
        <span id="{id}-wrapper" {attrs}>
            <span id="{id}-deck" class="deck">
                {choices}
            </span>
            <input type="text" name="{name}-autocomplete" id="{id}-autocomplete" value="" {input_attrs} />
            <select style="display:none" class="value-select" name="{name}" id="{id}" multiple="multiple">
                {options}
            </select>
            <span style="display:none" class="remove">ˣ</span>
            <span style="display:none" class="choice-template">
                <span class="choice prepend-remove append-option-html"></span>
            </span>
        </span>
        '''.format(
            id=attrs['id'],
            name=name,
            attrs=flatatt(self.build_attrs(attrs)),
            input_attrs=flatatt(self.build_input_attrs()),
            choices='',
            options='',
        )
        return mark_safe(html)

    def build_input_attrs(self, **kwargs):
        attrs = {
            'class': 'autocomplete vTextField',
            'data-autocomplete-choice-selector': '[data-value]',
            'data-autocomplete-url': self.url,
            'placeholder': _('type some text to search in this autocomplete'),
        }

        return attrs

    def build_attrs(self, *args, **kwargs):
        attrs = super(JalWidgetMixin, self).build_attrs(*args, **kwargs)

        if 'class' not in attrs:
            attrs['class'] = ''

        attrs['class'] += ' autocomplete-light-widget '

        if attrs.get('data-widget-maximum-values', 0) == 1:
            attrs['class'] += ' single'
        else:
            attrs['class'] += ' multiple'

        return attrs


class JalChoiceWidget(JalWidgetMixin, WidgetMixin, forms.Select):
    """
    Widget that provides an autocomplete for zero to one choice.
    """

    def __init__(self, url=None, forward=None, widget_attrs=None, *args,
                 **kwargs):
        forms.Select.__init__(self, *args, **kwargs)

        WidgetMixin.__init__(
            self,
            url=url,
            forward=forward
        )

        self.attrs.setdefault('data-widget-maximum-values', 1)
