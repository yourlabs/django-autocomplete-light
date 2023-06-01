from django import http
from dal.views import BaseQuerySetView



class AlightQuerySetView(BaseQuerySetView):
    def render_to_response(self, context):
        """Return a JSON response in Select2 format."""
        html = []
        for result in context['object_list']:
            html.append(f'''
            <div data-value="{self.get_result_value(result)}">
            {self.get_result_label(result)}
            </div>
            ''')

        return http.HttpResponse(html)
