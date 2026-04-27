from django import http
from django.utils.html import format_html, mark_safe
from dal.views import BaseQuerySetView


class AlightQuerySetView(BaseQuerySetView):
    def render_to_response(self, context):
        """Return an HTML fragment response for autocomplete-light."""
        html = []
        for result in context['object_list']:
            label = self.get_result_label(result)
            # template output is already HTML; plain __str__ must be escaped
            if self.template:
                label = mark_safe(label)
            html.append(format_html(
                '<div data-value="{}">{}</div>',
                self.get_result_value(result),
                label,
            ))
        return http.HttpResponse(
            ''.join(html),
            content_type='text/html; charset=utf-8',
        )
