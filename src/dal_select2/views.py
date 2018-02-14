"""Select2 view implementation."""

import collections
import json

from dal.views import BaseQuerySetView, ViewMixin

from django import http
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.translation import ugettext as _
from django.views.generic.list import View


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
                    'text': 'Create "%s"' % self.q,
                    'create_id': True
                }]
        return http.JsonResponse({
            'results': self.results(results) + create_option
        }, content_type='application/json')

    def autocomplete_results(self, results):
        """Return list of strings that match the autocomplete query."""
        return [x for x in results if self.q.lower() in x.lower()]

    def results(self, results):
        """Return the result dictionary."""
        return [dict(id=x, text=x) for x in results]

    def post(self, request):
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
        value = entry

        if isinstance(entry, collections.Sequence) and \
           not isinstance(entry, six.string_types):

            entry_length = len(entry)
            if(entry_length > 1):
                group, value = entry[0:2]
            elif(entry_length > 0):
                value = entry[0]

        if not isinstance(value, collections.Sequence) or \
           isinstance(value, six.string_types):
            value = (value,)

        return (group, value),

    def get(self, request, *args, **kwargs):
        """Return option list with children(s) json response."""
        results_dict = {}
        results = self.get_list()

        if results:
            flat_results = [(group, item) for entry in results
                            for group, items in self.get_item_as_group(entry)
                            for item in items]

            if self.q:
                q = self.q.lower()
                flat_results = [(g, x) for g, x in flat_results
                                if q in x.lower()]
            for group, value in flat_results:
                results_dict.setdefault(group, [])
                results_dict[group].append(value)

        return http.JsonResponse({
            "results":
                [{"id": x, "text": x} for x in results_dict.pop(None, [])] +
                [{"id": g, "text": g, "children": [{"id": x, "text": x}
                                                   for x in l]}
                 for g, l in six.iteritems(results_dict)]
        })
