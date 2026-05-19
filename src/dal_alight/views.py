from collections import OrderedDict

from django import http
from django.core.exceptions import ImproperlyConfigured
from django.db.models import F
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.views.generic.list import View

from dal.views import BaseQuerySetView, ViewMixin


class AlightQuerySetView(BaseQuerySetView):
    """Autocomplete view returning HTML fragments for autocomplete-light.

    Each result is rendered as ``<div data-value="{pk}">{label}</div>``.
    When ``create_field`` is set and the query has no case-insensitive exact
    match on page 1, a ``<div data-create>Create "…"</div>`` is appended.
    POST is handled by the inherited ``BaseQuerySetView.post()`` which creates
    the object and returns a ``<div data-value="…">…</div>`` HTML fragment.
    """

    case_sensitive_create = False

    def _should_show_create(self, context, q):
        if not self.create_field or not q:
            return False
        page_obj = context.get('page_obj')
        if page_obj and page_obj.number != 1:
            return False
        if not self.has_add_permission(self.request):
            return False
        existing = (self.get_result_label(r) for r in context['object_list'])
        if self.case_sensitive_create:
            return q not in existing
        q_lower = q.lower()
        return not any(label.lower() == q_lower for label in existing)

    def render_to_response(self, context):
        q = self.request.GET.get('q', '')
        html = []
        for result in context['object_list']:
            label = self.get_result_label(result)
            html.append(format_html(
                '<div data-value="{}">{}</div>',
                self.get_result_value(result),
                label,
            ))

        if self._should_show_create(context, q):
            html.append(format_html(
                '<div data-create data-value="{}">{}</div>',
                q,
                _('Create "%(new_value)s"') % {'new_value': q},
            ))

        if self.has_more(context):
            html.append(format_html(
                '<div data-next-page="{}">{}</div>',
                context['page_obj'].next_page_number(),
                _('More results…'),
            ))

        return http.HttpResponse(
            ''.join(html),
            content_type='text/html; charset=utf-8',
        )


class AlightGroupQuerySetView(AlightQuerySetView):
    """Grouped queryset view — mirrors Select2GroupQuerySetView.

    Results are rendered as::

        <div class="autocomplete-light-group">Group label</div>
        <div data-value="pk">Label</div>
        …

    Group header divs carry no ``data-value`` so the component treats them
    as non-selectable.
    """

    group_by_related = None
    related_field_name = 'name'

    def get_queryset(self):
        if not self.group_by_related:
            raise ImproperlyConfigured('Missing group_by_related.')
        return super().get_queryset().annotate(
            _group_name=F(f'{self.group_by_related}__{self.related_field_name}')
        )

    def render_to_response(self, context):
        groups = OrderedDict()
        for result in context['object_list']:
            groups.setdefault(getattr(result, '_group_name'), []).append(result)

        html = []
        for group_name, results in groups.items():
            html.append(format_html(
                '<div class="autocomplete-light-group">{}</div>',
                group_name or '',
            ))
            for result in results:
                label = self.get_result_label(result)
                html.append(format_html(
                    '<div data-value="{}">{}</div>',
                    self.get_result_value(result),
                    label,
                ))

        return http.HttpResponse(
            ''.join(html),
            content_type='text/html; charset=utf-8',
        )


class AlightListView(ViewMixin, View):
    """Autocomplete from a list of strings or (value, label) pairs.

    Mirrors ``Select2ListView`` but returns HTML fragments instead of JSON.

    Override ``get_list()`` to return your items.  Each item may be a plain
    string (value == label) or a ``(value, label)`` tuple/list.

    Define ``create(text)`` on the view to enable POST-based creation; it
    should return the created text/value or raise an error.
    """

    def get_list(self):
        return []

    def _parse_item(self, item):
        """Return (value, label) for a list item."""
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            return str(item[0]), str(item[1])
        return str(item), str(item)

    def get(self, request, *args, **kwargs):
        results = self.get_list()
        q = self.q

        if q:
            q_lower = q.lower()
            filtered = []
            for item in results:
                value, label = self._parse_item(item)
                if q_lower in label.lower():
                    filtered.append((value, label))
        else:
            filtered = [self._parse_item(item) for item in results]

        html = []
        for value, label in filtered:
            html.append(format_html(
                '<div data-value="{}">{}</div>', value, label,
            ))

        if q and hasattr(self, 'create'):
            html.append(format_html(
                '<div data-create data-value="{}">{}</div>',
                q,
                _('Create "%(new_value)s"') % {'new_value': q},
            ))

        return http.HttpResponse(
            ''.join(html),
            content_type='text/html; charset=utf-8',
        )

    def post(self, request, *args, **kwargs):
        if not hasattr(self, 'create'):
            return http.HttpResponse(status=405)

        text = request.POST.get('text', None)
        if text is None:
            return http.HttpResponseBadRequest()

        result = self.create(text)
        if result is None:
            return http.HttpResponseBadRequest()

        return http.HttpResponse(
            format_html('<div data-value="{}">{}</div>', result, result),
            content_type='text/html; charset=utf-8',
        )


class AlightTagAutocompleteView(AlightQuerySetView):
    """Convenience base for taggit tag autocomplete views.

    Returns ``result.name`` as the option value so ``TaggitAlight``
    can match tags by name rather than by PK.
    """

    def get_result_value(self, result):
        return result.name


class AlightGroupListView(AlightListView):
    """Grouped list view — mirrors Select2GroupListView.

    ``get_list()`` should return items of the form
    ``((group_id, group_label), [(value, label), …])`` or plain strings
    grouped by a leading group item.

    Simpler usage: return ``[(group, item), …]`` tuples where the first
    element is the group name and the second is the item string or
    ``(value, label)`` tuple.  Items with ``group=None`` are ungrouped.
    """

    def _parse_grouped(self, results):
        """Yield (group_name, value, label) triples."""
        for entry in results:
            if isinstance(entry, (list, tuple)) and len(entry) == 2:
                group, item = entry
                if isinstance(item, (list, tuple)):
                    # item is (value, label)
                    value, label = str(item[0]), str(item[1])
                else:
                    value = label = str(item)
                group_name = str(group) if group is not None else None
            else:
                group_name = None
                value = label = str(entry)
            yield group_name, value, label

    def get(self, request, *args, **kwargs):
        results = self.get_list()
        q = self.q
        q_lower = q.lower() if q else None

        groups = OrderedDict()
        for group_name, value, label in self._parse_grouped(results):
            if q_lower and q_lower not in label.lower():
                continue
            groups.setdefault(group_name, []).append((value, label))

        html = []
        ungrouped = groups.pop(None, [])
        for value, label in ungrouped:
            html.append(format_html('<div data-value="{}">{}</div>', value, label))
        for group_name, items in groups.items():
            html.append(format_html(
                '<div class="autocomplete-light-group">{}</div>', group_name,
            ))
            for value, label in items:
                html.append(format_html('<div data-value="{}">{}</div>', value, label))

        return http.HttpResponse(
            ''.join(html),
            content_type='text/html; charset=utf-8',
        )
