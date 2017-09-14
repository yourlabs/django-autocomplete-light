from __future__ import unicode_literals

from django import forms
from django.template.loader import render_to_string
from django.utils import safestring
from django.utils.translation import ugettext_lazy as _

"""
The provided widgets are meant to rely on an Autocomplete class.

- :py:class:`ChoiceWidget` :py:class:`django:django.forms.Select`

ChoiceWidget is intended to work as a replacement for django's Select widget,
and MultipleChoiceWidget for django's SelectMultiple,

Constructing a widget needs an Autocomplete class or registered autocomplete
name.

The choice autocomplete widget renders from autocomplete_light/widget.html
template.
"""


try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt


__all__ = ['WidgetBase', 'ChoiceWidget', 'MultipleChoiceWidget', 'TextWidget']


class WidgetBase(object):
    """
    Base widget for autocompletes.

    .. py:attribute:: attrs

        HTML ``<input />`` attributes, such as class, placeholder, etc ... Note
        that any ``data-autocomplete-*`` attribute will be parsed as an option
        for ``yourlabs.Autocomplete`` js object. For example::

        attrs={
            'placeholder': 'foo',
            'data-autocomplete-minimum-characters': 0
            'class': 'bar',
        }

        Will render like::
            <input
                placeholder="foo"
                data-autocomplete-minimum-characters="0"
                class="autocomplete bar"
            />

        Which will set by the way ``yourlabs.Autocomplete.minimumCharacters``
        option - the naming conversion is handled by jQuery.

    .. py:attribute:: widget_attrs

        HTML widget container attributes. Note that any ``data-widget-*``
        attribute will be parsed as an option for ``yourlabs.Widget`` js
        object. For example::

            widget_attrs={
                'data-widget-maximum-values': 6,
                'class': 'country-autocomplete',
            }

        Will render like::

            <span
                id="country-wrapper"
                data-widget-maximum-values="6"
                class="country-autocomplete autcomplete-light-widget"
            />

        Which will set by the way ``yourlabs.Widget.maximumValues`` - note that
        the naming conversion is handled by jQuery.

    .. py:attribute:: widget_js_attributes

        **DEPRECATED** in favor of :py:attr::`widget_attrs`.

        A dict of options that will override the default widget options. For
        example::

            widget_js_attributes = {'max_values': 8}

        The above code will set this HTML attribute::

            data-max-values="8"

        Which will override the default javascript widget maxValues option
        (which is 0).

        It is important to understand naming conventions which are sparse
        unfortunately:

        - python: lower case with underscores ie. ``max_values``,
        - HTML attributes: lower case with dashes ie. ``data-max-values``,
        - javascript: camel case, ie. ``maxValues``.

        The python to HTML name conversion is done by the
        autocomplete_light_data_attributes template filter.

        The HTML to javascript name conversion is done by the jquery plugin.

    .. py:attribute:: autocomplete_js_attributes

        **DEPRECATED** in favor of :py:attr::`attrs`.

        A dict of options like for :py:attr:`widget_js_attributes`. However,
        note that HTML attributes will be prefixed by ``data-autocomplete-``
        instead of just ``data-``. This allows the jQuery plugins to make the
        distinction between attributes for the autocomplete instance and
        attributes for the widget instance.

    .. py:attribute:: extra_context

        Extra context dict to pass to the template.

    .. py:attribute:: widget_template

        Template to use to render the widget. Default is
        ``autocomplete_light/widget.html``.
    """

    def __init__(self, autocomplete=None, widget_js_attributes=None,
                 autocomplete_js_attributes=None, extra_context=None,
                 registry=None, widget_template=None, widget_attrs=None):
        self._registry = registry
        self._autocomplete = None
        self.autocomplete_arg = autocomplete

        self.widget_js_attributes = widget_js_attributes or {}
        self.autocomplete_js_attributes = autocomplete_js_attributes or {}
        self.extra_context = extra_context or {}
        self.widget_template = (widget_template or
                'autocomplete_light/widget.html')
        self.widget_attrs = widget_attrs or {}

        if autocomplete_js_attributes is not None:
            raise PendingDeprecationWarning('autocomplete_js_attributes are'
                    'deprecated in favor of attrs')

        if widget_js_attributes is not None:
            raise PendingDeprecationWarning('widget_js_attributes are'
                    'deprecated in favor of widget_attrs')

    @property
    def registry(self):
        if self._registry is None:
            from autocomplete_light.registry import registry
            self._registry = registry
        return self._registry

    def render(self, name, value, attrs=None):
        widget_attrs = self.build_widget_attrs(name)

        autocomplete = self.autocomplete(values=value)

        attrs = self.build_attrs(self.attrs, attrs, autocomplete=autocomplete)

        self.html_id = attrs.pop('id', name)

        choices = autocomplete.choices_for_values()
        values = [autocomplete.choice_value(c) for c in choices]

        context = {
            'name': name,
            'values': values,
            'choices': choices,
            'widget': self,
            'attrs': safestring.mark_safe(flatatt(attrs)),
            'widget_attrs': safestring.mark_safe(flatatt(widget_attrs)),
            'autocomplete': autocomplete,
        }
        context.update(self.extra_context)

        template = getattr(autocomplete, 'widget_template',
                self.widget_template)
        return safestring.mark_safe(render_to_string(template, context))

    def build_attrs(self, attrs, extra_attrs=None,
                    autocomplete=None, **kwargs):
        attrs.copy()
        attrs.update(getattr(autocomplete, 'attrs', {}))
        attrs = super(WidgetBase, self).build_attrs(
            attrs, extra_attrs, **kwargs)

        if 'class' not in attrs.keys():
            attrs['class'] = ''

        attrs['class'] += ' autocomplete vTextField'

        attrs.setdefault('data-autocomplete-choice-selector', '[data-value]')
        attrs.setdefault('data-autocomplete-url',
                         self.autocomplete().get_absolute_url())
        attrs.setdefault('placeholder', _(
            'type some text to search in this autocomplete'))

        # for backward compatibility
        for key, value in self.autocomplete_js_attributes.items():
            attrs['data-autocomplete-%s' % key.replace('_', '-')] = value

        return attrs

    def build_widget_attrs(self, name=None):
        attrs = getattr(self.autocomplete, 'widget_attrs', {}).copy()
        attrs.update(self.widget_attrs)

        if 'class' not in attrs:
            attrs['class'] = ''

        attrs.setdefault('data-widget-bootstrap', 'normal')

        # for backward compatibility
        for key, value in self.autocomplete_js_attributes.items():
            attrs['data-widget-%s' % key.replace('_', '-')] = value

        attrs['class'] += ' autocomplete-light-widget '

        if name:
            attrs['class'] += name

        if attrs.get('data-widget-maximum-values', 0) == 1:
            attrs['class'] += ' single'
        else:
            attrs['class'] += ' multiple'

        return attrs

    def autocomplete():
        def fget(self):
            if not self._autocomplete:
                self._autocomplete = self.registry.get_autocomplete_from_arg(
                    self.autocomplete_arg)

            return self._autocomplete

        def fset(self, value):
            self._autocomplete = value
            self.autocomplete_name = value.__class__.__name__

        return {'fget': fget, 'fset': fset}
    autocomplete = property(**autocomplete())


class ChoiceWidget(WidgetBase, forms.Select):
    """
    Widget that provides an autocomplete for zero to one choice.
    """

    def __init__(self, autocomplete=None, widget_js_attributes=None,
            autocomplete_js_attributes=None, extra_context=None, registry=None,
            widget_template=None, widget_attrs=None, *args,
            **kwargs):

        forms.Select.__init__(self, *args, **kwargs)

        WidgetBase.__init__(self, autocomplete, widget_js_attributes,
                autocomplete_js_attributes, extra_context, registry,
                widget_template, widget_attrs)

        self.widget_attrs.setdefault('data-widget-maximum-values', 1)


class MultipleChoiceWidget(WidgetBase, forms.SelectMultiple):
    """
    Widget that provides an autocomplete for zero to n choices.
    """
    def __init__(self, autocomplete=None, widget_js_attributes=None,
            autocomplete_js_attributes=None, extra_context=None, registry=None,
            widget_template=None, widget_attrs=None, *args,
            **kwargs):

        forms.SelectMultiple.__init__(self, *args, **kwargs)

        WidgetBase.__init__(self, autocomplete,
            widget_js_attributes, autocomplete_js_attributes, extra_context,
            registry, widget_template, widget_attrs)


class TextWidget(WidgetBase, forms.TextInput):
    """
    Widget that just adds an autocomplete to fill a text input.

    Note that it only renders an ``<input>``, so attrs and widget_attrs are
    merged together.
    """

    def __init__(self, autocomplete=None, widget_js_attributes=None,
            autocomplete_js_attributes=None, extra_context=None, registry=None,
            widget_template=None, widget_attrs=None, *args,
            **kwargs):

        forms.TextInput.__init__(self, *args, **kwargs)

        WidgetBase.__init__(self, autocomplete, widget_js_attributes,
                autocomplete_js_attributes, extra_context, registry,
                widget_template, widget_attrs)

    def render(self, name, value, attrs=None):
        """ Proxy Django's TextInput.render() """

        autocomplete = self.autocomplete(values=value)
        attrs = self.build_attrs(self.attrs, attrs, autocomplete=autocomplete)

        return forms.TextInput.render(self, name, value, attrs)

    def build_attrs(self, attrs, extra_attrs=None,
                    autocomplete=None, **kwargs):
        attrs.copy()
        attrs.update(super(TextWidget, self).build_widget_attrs())
        attrs.update(getattr(autocomplete, 'attrs', {}))
        attrs.update(super(TextWidget, self).build_attrs(
            self.attrs, extra_attrs, **kwargs))

        def update_attrs(source, prefix=''):
            for key, value in source.items():
                key = 'data-%s%s' % (prefix, key.replace('_', '-'))
                attrs[key] = value

        update_attrs(self.widget_js_attributes, 'widget-')
        update_attrs(self.autocomplete_js_attributes, 'autocomplete-')

        attrs['data-widget-bootstrap'] = 'text'
        attrs['class'] += ' autocomplete-light-text-widget'

        return attrs
