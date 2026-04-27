from django import forms
from django.utils.html import format_html
from dal.widgets import QuerySetSelectMixin


class AlightWidgetMixin:
    component = 'autocomplete-select'

    @property
    def media(self):
        return forms.Media(
            css=dict(all=['dal_alight/autocomplete-light.css']),
            js=['dal_alight/autocomplete-light.js'],
        )

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        self.choices.field.empty_label = None
        attrs = attrs or {}
        attrs.setdefault('slot', 'select')
        widget = super().render(name, value, attrs=attrs, renderer=renderer, **kwargs)
        deck = '<div slot="deck"></div>'
        input = format_html(
            '<autocomplete-select-input slot="input" url="{}">'
            '<input name="{}-input" slot="input" class="vTextField" />'
            '</autocomplete-select-input>',
            self.url,
            name,
        )
        return widget + deck + input


class ModelAlight(QuerySetSelectMixin, AlightWidgetMixin, forms.Select):
    pass
