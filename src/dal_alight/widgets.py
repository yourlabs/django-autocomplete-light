from django import forms
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
        input = (
            f'<autocomplete-select-input slot="input" url="{self.url}">'
            f'<input name="{name}-input" slot="input" class="vTextField" />'
            f'</autocomplete-select-input>'
        )
        return widget + deck + input


class ModelAlight(QuerySetSelectMixin, AlightWidgetMixin, forms.Select):
    pass
