import django
from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget
from django.forms.widgets import ChoiceWidget
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from dal.widgets import QuerySetSelectMixin, WidgetMixin


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

    def __init__(self, *args, **kwargs):
        # AlightChoiceMixin.__init__ reaches Widget directly, skipping
        # AdminTextInputWidget.__init__, so apply the default class here.
        attrs = dict(kwargs.get('attrs') or {})
        attrs.setdefault('class', 'vTextField')
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)

    @property
    def media(self):
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

    def _get_input_placeholder(self, name):
        field = getattr(getattr(self, 'choices', None), 'field', None)
        label = getattr(field, 'label', None)
        if label:
            return label
        return name

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

    def _render_search_input(self, name, attrs, renderer=None, **kwargs):
        """Render the visible search input; attrs apply like any TextInput.

        Use a dedicated ``AdminTextInputWidget`` instance so
        ``ChoiceWidget.format_value`` does not format the search value.
        """
        # BoundField attrs include field-level keys (e.g. required) that apply
        # to submitted values, not the auxiliary search box.
        excluded = frozenset({'required', 'aria-describedby', 'name'})
        search_attrs = {
            k: v for k, v in {**self.attrs, **(attrs or {})}.items()
            if k not in excluded
        }
        search_attrs.update({
            'slot': 'input',
            'autocomplete': 'off',
        })
        search_attrs.setdefault(
            'placeholder', self._get_input_placeholder(name),
        )
        return AdminTextInputWidget().render(
            f'{name}-input',
            '',
            attrs=search_attrs,
            renderer=renderer,
            **kwargs,
        )

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        if hasattr(self.choices, 'field'):
            self.choices.field.empty_label = None
        attrs = attrs or {}
        field_id = attrs.get('id') or name

        values_html, deck_html = self._render_values_and_deck(
            name, value, attrs=attrs
        )

        url_attr = format_html(' url="{}"', self.url) if self.url else ''
        input_html = self._render_search_input(
            name, attrs, renderer=renderer, **kwargs
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
    AlightChoiceMixin,
    AdminTextInputWidget,
):
    """Single-select autocomplete widget backed by a QuerySet."""


class ModelAlightMultiple(
    QuerySetSelectMixin,
    AlightWidgetMixin,
    AlightMultipleMixin,
    AlightChoiceMixin,
    AdminTextInputWidget,
):
    """Multi-select autocomplete widget backed by a QuerySet."""


# ---------------------------------------------------------------------------
# Non-queryset widgets (arbitrary choice lists)
# ---------------------------------------------------------------------------

class Alight(
    _AlightUrlRequiredMixin,
    AlightWidgetMixin,
    WidgetMixin,
    AlightChoiceMixin,
    AdminTextInputWidget,
):
    """Single-select autocomplete for arbitrary choices.

    Requires a ``url`` — results are always fetched from the autocomplete view.
    """


class AlightMultiple(
    _AlightUrlRequiredMixin,
    AlightWidgetMixin,
    WidgetMixin,
    AlightMultipleMixin,
    AlightChoiceMixin,
    AdminTextInputWidget,
):
    """Multiple-select autocomplete for arbitrary choices."""


class ListAlight(
    _AlightUrlRequiredMixin,
    AlightWidgetMixin,
    WidgetMixin,
    AlightChoiceMixin,
    AdminTextInputWidget,
):
    """Single-select autocomplete backed by ``AlightListView``.

    Use alongside ``AlightListView`` on the server.
    """


# ---------------------------------------------------------------------------
# Tag widget
# ---------------------------------------------------------------------------

class TagAlight(
    AlightWidgetMixin,
    WidgetMixin,
    AlightMultipleMixin,
    AlightChoiceMixin,
    AdminTextInputWidget,
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
        if value and ',' not in value:
            value = '%s,' % value
        return value

    def option_value(self, value):
        return value.tag.name if hasattr(value, 'tag') else value
