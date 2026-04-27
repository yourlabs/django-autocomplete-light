from django import http
from dal.views import BaseQuerySetView


class AlightQuerySetView(BaseQuerySetView):
    def render_to_response(self, context):
        """Return an HTML fragment response for autocomplete-light."""
        html = []
        for result in context['object_list']:
            html.append(
                f'<div data-value="{self.get_result_value(result)}">'
                f'{self.get_result_label(result)}'
                f'</div>'
            )
        return http.HttpResponse(
            ''.join(html),
            content_type='text/html; charset=utf-8',
        )
