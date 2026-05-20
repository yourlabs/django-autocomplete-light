from django import forms
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from dal.widgets import QuerySetSelectMixin, WidgetMixin


def _is_iterable(x):
    try:
        iter(x)
    except TypeError:
        return False
    return True


class AlightWidgetMixin:
    """Mixin that renders the autocomplete-light web component shell.

    Wraps the underlying ``<select>`` (rendered by ``super().render()``) in::

        <autocomplete-select>
          <select slot="select">…</select>
          <div slot="deck"></div>
          <autocomplete-select-input slot="input" [url="…"]>
            <input …/>
          </autocomplete-select-input>
          <!-- dal-forward-conf div injected by WidgetMixin.render() -->
        </autocomplete-select>
    """

    # Read by dal.widgets.WidgetMixin.render() (called via MRO after this
    # mixin) to wrap the slot trio in <autocomplete-select>…</autocomplete-select>.
    component = 'autocomplete-select'

    @property
    def media(self):
        return forms.Media(
            css=dict(all=['dal_alight/autocomplete-light.css']),
            js=['dal_alight/autocomplete-light.js', 'dal_alight/dal-django.js'],
        )

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        if hasattr(self.choices, 'field'):
            self.choices.field.empty_label = None
        attrs = attrs or {}
        attrs.setdefault('slot', 'select')

        widget = super().render(name, value, attrs=attrs, renderer=renderer, **kwargs)

        deck = '<span slot="deck"></span>'
        url_attr = format_html(' url="{}"', self.url) if self.url else ''
        input_widget = forms.TextInput(attrs={
            'name': f'{name}-input',
            'slot': 'input',
            'class': 'vTextField',
            'placeholder': _('Search'),
            'autocomplete': 'off',
        })
        input_html = input_widget.render(f'{name}-input', '', renderer=renderer)
        input_el = format_html(
            '<autocomplete-select-input slot="input"{}>{}</autocomplete-select-input>',
            url_attr,
            input_html,
        )
        return widget + deck + str(input_el)


# ---------------------------------------------------------------------------
# Queryset-backed widgets (FK / M2M)
# ---------------------------------------------------------------------------

class ModelAlight(
    QuerySetSelectMixin,
    AlightWidgetMixin,
    forms.Select,
):
    """Single-select autocomplete widget backed by a QuerySet."""


class ModelAlightMultiple(
    QuerySetSelectMixin,
    AlightWidgetMixin,
    forms.SelectMultiple,
):
    """Multi-select autocomplete widget backed by a QuerySet."""


# ---------------------------------------------------------------------------
# Non-queryset widgets (arbitrary choice lists)
# ---------------------------------------------------------------------------

class Alight(WidgetMixin, AlightWidgetMixin, forms.Select):
    """Single-select autocomplete for arbitrary choices.

    Without a ``url`` the component filters ``<option>`` elements locally in
    JS — no server round-trip needed.  With a ``url`` it fetches from the
    view as usual.
    """


class AlightMultiple(WidgetMixin, AlightWidgetMixin, forms.SelectMultiple):
    """Multiple-select autocomplete for arbitrary choices."""


class ListAlight(WidgetMixin, AlightWidgetMixin, forms.Select):
    """Single-select autocomplete backed by ``AlightListView``.

    Use alongside ``AlightListView`` on the server.
    """


# ---------------------------------------------------------------------------
# Tag widget
# ---------------------------------------------------------------------------

class TagAlight(WidgetMixin, AlightWidgetMixin, forms.SelectMultiple):
    """Free-text tag widget — value stored as comma-separated text.

    AlightInitialRenderMixin is intentionally omitted: tags are not PKs so
    the queryset-filter approach would break; optgroups() handles initial
    values directly via _iter_tag_values().

    Tags are not backed by a model: the tag text IS the option value.
    Use alongside ``AlightListView`` with a ``create()`` method, or any view
    that returns HTML fragments.

    The stored field value is a comma-separated string (same as TagSelect2).
    """

    def option_value(self, value):
        return value

    def format_value(self, value):
        if not isinstance(value, (tuple, list)):
            value = [value]
        values = set()
        for v in value:
            if not v:
                continue
            if isinstance(v, str):
                parts = v.split(',')
            elif _is_iterable(v):
                parts = v
            else:
                parts = [v]
            for part in parts:
                values.add(self.option_value(str(part).strip()))
        return values

    def _iter_tag_values(self, value):
        """Yield individual tag strings from a raw value."""
        if isinstance(value, str):
            value = value.split(',')
        for v in value:
            if not v:
                continue
            yield self.option_value(str(v).strip())

    def optgroups(self, name, value, attrs=None):
        default = (None, [], 0)
        groups = [default]
        for i, v in enumerate(self._iter_tag_values(value)):
            default[1].append(self.create_option(v, v, v, True, i))
        return groups

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return ','.join(values)


class TaggitAlight(TagAlight):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        # trailing comma keeps multi-word single tags intact for taggit's parser
        if value and ',' not in value:
            value = '%s,' % value
        return value

    def option_value(self, value):
        # taggit may yield TaggedItem objects on initial render
        return value.tag.name if hasattr(value, 'tag') else value
