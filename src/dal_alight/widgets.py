from django import forms
from django.urls import reverse
from dal.widgets import (
    QuerySetSelectMixin,
)


class AlightWidgetMixin:
    component = 'autocomplete-select'

    @property
    def media(self):
        return forms.Media(
            css=dict(all=['dal_alight/autocomplete-light.css']),
            js=['dal_alight/autocomplete-light.js'],
        )

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        # this prevents ModelChoiceIterator from rendering empty option that we
        # don't need with autocompletes
        self.choices.field.empty_label = None

        attrs = attrs or {}
        attrs.setdefault('slot', 'select')
        widget = super().render(name, value, attrs=attrs, renderer=renderer,
                                **kwargs)
        deck = '<div slot="deck"></div>'
        input = f'''
        <autocomplete-select-input slot="input" url="{self.url}">
            <input name="{name}-input" slot="input" class="vTextField" />
        </autocomplete-select-input>
        '''
        html = widget + deck + input
        return html



class ModelAlight(QuerySetSelectMixin,
                  AlightWidgetMixin,
                  forms.Select):
    pass
