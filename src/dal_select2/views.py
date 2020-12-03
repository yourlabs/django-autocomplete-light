"""Select2 view implementation."""

import collections
# import json

from dal.views import BaseQuerySetView, ViewMixin

from django import http
from django.core.exceptions import ImproperlyConfigured
from django.db.models import F
from django.utils.translation import ugettext as _
from django.views.generic.list import View

import six


class Select2ViewMixin(object):
    """View mixin to render a JSON response for Select2."""

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return [
            {
                'id': self.get_result_value(result),
                'text': self.get_result_label(result),
                'selected_text': self.get_selected_result_label(result),
            } for result in context['object_list']
        ]

    def get_create_option(self, context, q):
        """Form the correct create_option to append to results."""
        create_option = []
        display_create_option = False
        if self.create_field and q:
            page_obj = context.get('page_obj', None)
            if page_obj is None or page_obj.number == 1:
                display_create_option = True

            # Don't offer to create a new option if a
            # case-insensitive) identical one already exists
            existing_options = (self.get_result_label(result).lower()
                                for result in context['object_list'])
            if q.lower() in existing_options:
                display_create_option = False

        if display_create_option and self.has_add_permission(self.request):
            create_option = [{
                'id': q,
                'text': _('Create "%(new_value)s"') % {'new_value': q},
                'create_id': True,
            }]
        return create_option

    def render_to_response(self, context):
        """Return a JSON response in Select2 format."""
        q = self.request.GET.get('q', None)

        create_option = self.get_create_option(context, q)

        return http.JsonResponse(
            {
                'results': self.get_results(context) + create_option,
                'pagination': {
                    'more': self.has_more(context)
                }
            })


class Select2QuerySetView(Select2ViewMixin, BaseQuerySetView):
    """List options for a Select2 widget."""


class Select2GroupQuerySetView(Select2QuerySetView):
    """List of grouped options for a Select2 widget.

    .. py:attribute:: group_by_related

        Name of the field for the related Model on a One to Many relation

    .. py:attribute:: related_field_name

        Name of the related Model field to run filter against.
    """

    group_by_related = None
    related_field_name = 'name'

    def get_results(self, context):
        """Return the options grouped by a common related model.

        Raises ImproperlyConfigured if self.group_by_name is not configured
        """
        if not self.group_by_related:
            raise ImproperlyConfigured("Missing group_by_related.")

        groups = collections.OrderedDict()

        object_list = context['object_list']
        object_list = object_list.annotate(
            group_name=F(f'{self.group_by_related}__{self.related_field_name}'))

        for result in object_list:
            group_name = getattr(result, 'group_name')
            groups.setdefault(group_name, [])
            groups[group_name].append(result)

        return [{
            'id': None,
            'text': group,
            'children': [{
                'id': result.id,
                'text': getattr(result, self.related_field_name),
                'title': result.descricao
            } for result in results]
        } for group, results in groups.items()]


class Select2ListView(ViewMixin, View):
    """Autocomplete from a list of items rather than a QuerySet."""

    def get_list(self):
        """Return the list strings from which to autocomplete."""
        return []

    def get(self, request, *args, **kwargs):
        """Return option list json response."""
        results = self.get_list()
        create_option = []
        if self.q:
            results = self.autocomplete_results(results)
            if hasattr(self, 'create'):
                create_option = [{
                    'id': self.q,
                    'text': _('Create "%(new_value)s"') % {
                        'new_value': self.q
                    },
                    'create_id': True
                }]
        return http.JsonResponse({
            'results': self.results(results) + create_option
        }, content_type='application/json')

    def autocomplete_results(self, results):
        """Return list of strings that match the autocomplete query."""
        if all(isinstance(el, list) for el in results) and len(results) > 0:
            return [[x, y] for [x, y] in results if self.q.lower() in y.lower()]
        if all(isinstance(el, tuple) for el in results) and len(results) > 0:
            return [[x, y] for (x, y) in results if self.q.lower() in y.lower()]
        else:
            return [x for x in results if self.q.lower() in x.lower()]

    def results(self, results):
        """Return the result dictionary."""
        if all(isinstance(el, list) for el in results) and len(results) > 0:
            return [dict(id=x, text=y) for [x, y] in results]
        elif all(isinstance(el, tuple) for el in results) and len(results) > 0:
            return [dict(id=x, text=y) for (x, y) in results]
        else:
            return [dict(id=x, text=x) for x in results]

    def post(self, request, *args, **kwargs):
        """Add an option to the autocomplete list.

        If 'text' is not defined in POST or self.create(text) fails, raises
        bad request. Raises ImproperlyConfigured if self.create if not defined.
        """
        if not hasattr(self, 'create'):
            raise ImproperlyConfigured('Missing "create()"')

        text = request.POST.get('text', None)

        if text is None:
            return http.HttpResponseBadRequest()

        text = self.create(text)

        if text is None:
            return http.HttpResponseBadRequest()

        return http.JsonResponse({
            'id': text,
            'text': text,
        })


class Select2GroupListView(Select2ListView):
    """View mixin for grouped options."""

    def get_item_as_group(self, entry):
        """Return the item with its group."""
        group = None
        item = entry

        if isinstance(entry, collections.Sequence) and \
           not isinstance(entry, six.string_types):

            entry_length = len(entry)

            if all(isinstance(el, list) for el in entry) and entry_length > 1:
                group, item = entry[0:2]
                return (group, item),
            elif all(isinstance(el, list) for el in entry) and entry_length > 1:
                group, item = entry[0:2]
                return (group, item),

            else:
                if(entry_length > 1):
                    group, item = entry[0:2]
                elif(entry_length > 0):
                    item = entry[0]

        if not isinstance(item, collections.Sequence) or \
           isinstance(item, six.string_types):
            item = (item,)

        return (group, item),

    def get(self, request, *args, **kwargs):
        """Return option list with children(s) json response."""
        results_dict = {}
        results = self.get_list()

        if results:
            if (
                all(isinstance(el, list) for el in results)
                or all(isinstance(el, tuple) for el in results)
            ):
                flat_results = [
                    (group[0], group[1], item[0], item[1]) for entry in results
                    for group, items in self.get_item_as_group(entry)
                    for item in items
                ]

                if self.q:
                    q = self.q.lower()
                    flat_results = [(g, h, x, y) for g, h, x, y in flat_results
                                    if q in y.lower()]
                for group_id, group, item_id, item in flat_results:
                    results_dict.setdefault((group_id, group), [])
                    results_dict[(group_id, group)].append([item_id, item])

                return http.JsonResponse({
                    "results": [
                        {
                            "id": x, "text": y
                        } for x, y in results_dict.pop((None, None), [])
                    ] + [
                        {
                            "id": g[0],
                            "text": g[1],
                            "children": [
                                {"id": x, "text": y} for x, y in l
                            ]
                        }
                        for g, l in six.iteritems(results_dict)
                    ]
                })

            else:
                flat_results = [(group, item) for entry in results
                                for group, items in self.get_item_as_group(entry)
                                for item in items]

                if self.q:
                    q = self.q.lower()
                    flat_results = [(g, x) for g, x in flat_results
                                    if q in x.lower()]
                for group, item in flat_results:
                    results_dict.setdefault(group, [])
                    results_dict[group].append(item)

                return http.JsonResponse({
                    "results": [
                        {"id": x, "text": x} for x in results_dict.pop(None, [])
                    ] + [
                        {
                            "id": g,
                            "text": g,
                            "children": [
                                {"id": x, "text": x} for x in l
                            ]
                        }
                        for g, l in six.iteritems(results_dict)
                    ]
                })
