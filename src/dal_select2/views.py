"""Select2 view implementation."""

import json

from dal.views import BaseQuerySetView

from django import http


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
