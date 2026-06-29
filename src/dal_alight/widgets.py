from django import forms
from django.forms.widgets import ChoiceWidget
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from dal.widgets import QuerySetSelectMixin, WidgetMixin

from .media import alight_media


def _is_iterable(x):
    try:
        iter(x)
    except TypeError:
        return False
    return True


class AlightChoiceMixin(ChoiceWidget):
    """Choice plumbing for Alight widgets; rendering is in AlightWidgetMixin."""

    # ChoiceWidget sets template_name = None; keep TextInput rendering working.
    template_name = 'django/forms/widgets/text.html'
    input_type = 'text'

    def get_context(self, name, value, attrs):
        """Text input context for the search field (no ChoiceWidget optgroups)."""
        context = super(ChoiceWidget, self).get_context(name, value, attrs)
        # Search input is always empty; ChoiceWidget.format_value would list-wrap.
        context["widget"]["value"] = forms.TextInput.format_value(self, value)
        return context


class AlightMultipleMixin:
    """Multiple-selection behaviour for hidden value inputs."""

    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        try:
            return data.getlist(name)
        except AttributeError:
            val = data.get(name)
            if val is None:
                return []
            if isinstance(val, list):
                return val
            return [val]


class AlightWidgetMixin:
    """Mixin that renders the autocomplete-light web component shell.

    The visible search field is a ``TextInput``; callers configure it with the
    usual widget ``attrs``.  Selected values are stored in hidden
    ``slot="values"`` inputs.
    """

    @property
    def media(self):
        return alight_media()

    def _iter_selected_options(self, name, value, attrs=None):
        """Yield selected options as flat dicts for deck/hidden inputs.

        Alight has no optgroup UI; this hides Django's grouped optgroups() API.
        """
        for _group, options, _index in self.optgroups(name, value, attrs=attrs):
            for option in options:
                if not option['selected']:
                    continue
                val = option['value']
                if val is None or val == '':
                    continue
                yield option

    def _render_values_and_deck(self, name, value, attrs=None):
        """Build hidden inputs and deck chips for the current selection."""
        value = self.format_value(value)
        hidden_parts = []
        deck_parts = []
        disabled = mark_safe(' disabled') if attrs and attrs.get('disabled') else ''
        for option in self._iter_selected_options(name, value, attrs=attrs):
            val = option['value']
            label = option['label']
            hidden_parts.append(format_html(
                '<input type="hidden" name="{}" value="{}" slot="values" '
                'data-label="{}"{}>',
                name,
                val,
                label,
                disabled,
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

    def _render_search_input(self, name, attrs, renderer=None, **kwargs):
        """Render the visible search input via the TextInput ``render()`` MRO."""
        # BoundField puts ``required`` in attrs for the field widget.  The search
        # input is auxiliary (values submit via hidden inputs); strip it so the
        # browser does not run HTML5 validation on an empty search box.
        search_attrs = {k: v for k, v in attrs.items() if k != 'required'}
        search_attrs['slot'] = 'input'
        search_attrs['autocomplete'] = 'off'
        return super(AlightChoiceMixin, self).render(
            f'{name}-input',
            '',
            attrs=search_attrs,
            renderer=renderer,
            **kwargs,
        )

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        if hasattr(self.choices, 'field'):
            self.choices.field.empty_label = None
        final_attrs = self.build_attrs(self.attrs, attrs)
        field_id = final_attrs.get('id') or name

        values_html, deck_html = self._render_values_and_deck(
            name, value, attrs=final_attrs
        )

        url_attr = format_html(' url="{}"', self.url) if self.url else ''
        input_html = self._render_search_input(
            name, final_attrs, renderer=renderer, **kwargs
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


# ---------------------------------------------------------------------------
# Queryset-backed widgets (FK / M2M)
# ---------------------------------------------------------------------------

class ModelAlight(
    AlightWidgetMixin,
    QuerySetSelectMixin,
    AlightChoiceMixin,
    forms.TextInput,
):
    """Single-select autocomplete widget backed by a QuerySet."""


class ModelAlightMultiple(
    AlightWidgetMixin,
    QuerySetSelectMixin,
    AlightMultipleMixin,
    AlightChoiceMixin,
    forms.TextInput,
):
    """Multi-select autocomplete widget backed by a QuerySet."""


# ---------------------------------------------------------------------------
# List-backed widgets (non-queryset)
# ---------------------------------------------------------------------------

class ListAlight(
    AlightWidgetMixin,
    WidgetMixin,
    AlightChoiceMixin,
    forms.TextInput,
):
    """Single-select autocomplete backed by ``AlightListView``.

    Use alongside ``AlightListView`` on the server.
    """

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
# Tag widget
# ---------------------------------------------------------------------------

class TagAlight(
    AlightWidgetMixin,
    WidgetMixin,
    AlightMultipleMixin,
    AlightChoiceMixin,
    forms.TextInput,
):
    """Free-text tag widget — value stored as comma-separated text.

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

    def _iter_selected_options(self, name, value, attrs=None):
        for v in self._iter_tag_values(value):
            yield {'value': v, 'label': v, 'selected': True}

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return ','.join(values)


class TaggitAlight(TagAlight):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if value and ',' not in value:
            value = '%s,' % value
        return value

    def option_value(self, value):
        return value.tag.name if hasattr(value, 'tag') else value
