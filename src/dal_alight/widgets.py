import django
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
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

    Wraps hidden value inputs and the search field in::

        <autocomplete-select>
          <input type="hidden" name="{field}" value="…" slot="values" …>
          <span slot="deck">…</span>
          <autocomplete-select-input slot="input" url="…">
            <input id="id_{field}" slot="input" …/>
          </autocomplete-select-input>
          <div class="dal-forward-conf">…</div>
        </autocomplete-select>
    """

    @property
    def media(self):
        # Django 6+ forms.Media supports Script(type="module"), which ensures
        # each URL executes once when multiple widgets merge media
        # (customElements.define must not run twice).  On older Django versions
        # we fall back to plain script paths.
        if django.VERSION >= (6, 0):
            from django.forms.widgets import Script

            js = [
                Script('dal_alight/autocomplete-light.js', type='module'),
                Script('dal_alight/dal-django.js', type='module'),
            ]
        else:
            js = [
                'dal_alight/autocomplete-light.js',
                'dal_alight/dal-django.js',
            ]
        return forms.Media(
            css=dict(all=['dal_alight/autocomplete-light.css']),
            js=js,
        )

    def _render_values_and_deck(self, name, value, attrs=None):
        """Build hidden inputs and deck chips for the current selection."""
        value = self.format_value(value)
        hidden_parts = []
        deck_parts = []
        for _group_name, group_options, _group_index in self.optgroups(
            name, value, attrs=attrs
        ):
            for option in group_options:
                if not option['selected']:
                    continue
                val = option['value']
                if val is None or val == '':
                    continue
                label = option['label']
                hidden_parts.append(format_html(
                    '<input type="hidden" name="{}" value="{}" slot="values" '
                    'data-label="{}">',
                    name,
                    val,
                    label,
                ))
                deck_parts.append(format_html(
                    '<div data-value="{}">{}</div>',
                    val,
                    label,
                ))
        values_html = mark_safe(''.join(hidden_parts))
        if deck_parts:
            deck_html = format_html(
                '<span slot="deck">{}</span>',
                mark_safe(''.join(deck_parts)),
            )
        else:
            deck_html = '<span slot="deck"></span>'
        return values_html, deck_html

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        if hasattr(self.choices, 'field'):
            self.choices.field.empty_label = None
        attrs = attrs or {}
        field_id = attrs.get('id') or name

        values_html, deck_html = self._render_values_and_deck(
            name, value, attrs=attrs
        )

        url_attr = format_html(' url="{}"', self.url) if self.url else ''
        input_widget = forms.TextInput()
        input_html = input_widget.render(
            f'{name}-input',
            '',
            attrs={
                'id': field_id,
                'slot': 'input',
                'class': 'vTextField',
                'placeholder': _('Search'),
                'autocomplete': 'off',
            },
            renderer=renderer,
        )
        input_el = format_html(
            '<autocomplete-select-input slot="input"{}>{}</autocomplete-select-input>',
            url_attr,
            input_html,
        )
        conf = self.render_forward_conf(field_id)

        multiple_attr = (
            ' data-multiple' if getattr(self, 'allow_multiple_selected', False) else ''
        )
        inner = values_html + deck_html + str(input_el) + conf
        return mark_safe(format_html(
            '<autocomplete-select{}>{}</autocomplete-select>',
            mark_safe(multiple_attr),
            mark_safe(inner),
        ))


class _AlightUrlRequiredMixin:
    """Choice widgets that always fetch from the server must have a url."""

    def __init__(self, url=None, *args, **kwargs):
        if url is None and args and isinstance(args[0], str):
            url = args[0]
        if not url:
            raise ValueError(
                '{} requires a url; client-side local filtering was removed.'
                .format(self.__class__.__name__)
            )
        super().__init__(url, *args, **kwargs)


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

class Alight(_AlightUrlRequiredMixin, WidgetMixin, AlightWidgetMixin, forms.Select):
    """Single-select autocomplete for arbitrary choices.

    Requires a ``url`` — results are always fetched from the autocomplete view.
    """


class AlightMultiple(
    _AlightUrlRequiredMixin,
    WidgetMixin,
    AlightWidgetMixin,
    forms.SelectMultiple,
):
    """Multiple-select autocomplete for arbitrary choices."""


class ListAlight(_AlightUrlRequiredMixin, WidgetMixin, AlightWidgetMixin, forms.Select):
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
