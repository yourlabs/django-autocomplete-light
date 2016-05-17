"""Autocomplete widgets bases."""

import copy

from django import VERSION
from django import forms
from django.core.urlresolvers import reverse
from django.utils import six


class WidgetMixin(object):
    """Base mixin for autocomplete widgets.

    .. py:attribute:: url

        Absolute URL to the autocomplete view for the widget. It can be set to
        a a URL name, in which case it will be reversed when the attribute is
        accessed.

    .. py:attribute:: forward

        List of field names to forward to the autocomplete view, useful to
        filter results using values of other fields in the form.

    .. py:attribute:: autocomplete_function

        Identifier of the javascript callback that should be
        executed when such a widget is loaded in the DOM,
        either on page load or dynamically.
    """

    def __init__(self, url=None, forward=None, *args, **kwargs):
        """Instanciate a widget with a URL and a list of fields to forward."""
        self.url = url
        self.forward = forward or []
        super(WidgetMixin, self).__init__(*args, **kwargs)

    def build_attrs(self, *args, **kwargs):
        """Build HTML attributes for the widget."""
        attrs = super(WidgetMixin, self).build_attrs(*args, **kwargs)

        if self.url is not None:
            attrs['data-autocomplete-light-url'] = self.url

        autocomplete_function = getattr(self, 'autocomplete_function', None)
        if autocomplete_function:
            attrs.setdefault('data-autocomplete-light-function',
                             autocomplete_function)

        if self.forward:
            attrs.setdefault('data-autocomplete-light-forward',
                             ','.join(self.forward))

        return attrs

    def filter_choices_to_render(self, selected_choices):
        """Replace self.choices with selected_choices."""
        self.choices = [c for c in self.choices if
                        six.text_type(c[0]) in selected_choices]

    def render_options(self, *args):
        """
        Django-compatibility method for option rendering.

        Should only render selected options, by setting self.choices before
        calling the parent method.
        """
        selected_choices_arg = 1 if VERSION < (1, 10) else 0

        # Filter out None values, not needed for autocomplete
        selected_choices = [c for c in args[selected_choices_arg] if c]

        if self.url:
            all_choices = copy.copy(self.choices)
            self.filter_choices_to_render(selected_choices)

        html = super(WidgetMixin, self).render_options(*args)

        if self.url:
            self.choices = all_choices

        return html

    def _get_url(self):
        if self._url is None:
            return None

        if '/' in self._url:
            return self._url

        return reverse(self._url)

    def _set_url(self, url):
        self._url = url

    url = property(_get_url, _set_url)


class Select(WidgetMixin, forms.Select):
    """Replacement for Django's Select to render only selected choices."""


class SelectMultiple(WidgetMixin, forms.SelectMultiple):
    """Replacement SelectMultiple to render only selected choices."""


class QuerySetSelectMixin(WidgetMixin):
    """QuerySet support for choices."""

    def filter_choices_to_render(self, selected_choices):
        """Filter out un-selected choices if choices is a QuerySet."""
        self.choices.queryset = self.choices.queryset.filter(
            pk__in=[c for c in selected_choices if c]
        )
