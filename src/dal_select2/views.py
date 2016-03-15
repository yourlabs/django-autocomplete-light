"""Select2 view implementation."""

import json

from dal.views import BaseQuerySetView, ViewMixin

from django import http
from django.views.generic.list import View, BaseListView


class Select2ViewMixin(object):
    """View mixin to render a JSON response for Select2."""

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return [
            {
                'id': self.get_result_value(result),
                'text': self.get_result_label(result),
            } for result in context['object_list']
        ]

    def render_to_response(self, context):
        """Return a JSON response in Select2 format."""
        create_option = []

        q = self.request.GET.get('q', None)
        if self.create_field and q and context['page_obj'].number == 1:
            create_option = [{
                'id': q,
                'text': 'Create "%s"' % q,
                'create_id': True,
            }]

        return http.HttpResponse(
            json.dumps({
                'results': self.get_results(context) + create_option,
                'pagination': {
                    'more': self.has_more(context)
                }
            }),
            content_type='application/json',
        )


class Select2QuerySetView(Select2ViewMixin, BaseQuerySetView):
    """List options for a Select2 widget."""

class Select2ListView(ViewMixin, View):
    """Autocomplete from a list of items rather than a QuerySet.
    get_list() should return a list of strings that may be autocopleted.
    """

    create_field = False
    """Set create_field to True to allow creation of new items."""

    def get_list(self):
        """"Return the list strings from which to autocomplete."""
        return []

    def get(self, request, *args, **kwargs):
        results = self.get_list()
        create_option = []
        if self.q:
            results = [ x for x in results if self.q in x ]
            if self.create_field:
                create_option = [{
                        'id': self.q,
                        'text': 'Create "%s"' % self.q,
                        'create_id': True
                    }]
        return http.HttpResponse(json.dumps({
            'results': [dict(id=x, text=x) for x in results] + create_option
        }))

    def create(self, text):
        """"Create a new list item for text.  None can be returned if the
        item may not be created for some reason."""
        return text

    def post(self, request):
        text = request.POST.get('text', None)
        if text is None:
            return http.HttpResponseBadRequest()
        text = self.create(text)
        if text is None:
            return http.HttpResponseBadRequest()
        return http.HttpResponse(json.dumps({
            'id': text,
            'text': text,
        }))
