from dal.views import BaseQuerySetView, ViewMixin

from django.views import generic


class JalQuerySetViewMixin(object):
    """View mixin to render a JSON response for Select2."""
    template_name_suffix = '_autocomplete'

    def get_result_html(self, result):
        '''Return the HTML for an otion, used by the widget too.'''
        return '<span data-value="{}">{}</span>'.format(
            self.get_result_value(result),
            self.get_result_label(result),
        )

    def render_to_response(self, context):
        q = self.request.GET.get('q', None)
        create_option = self.get_create_option(context, q)

        return http.HttpResponse(''.join([
            self.get_result_html(result)
            for result in self.get_results(context) + create_option
        ]))


class JalQuerySetView(JalQuerySetViewMixin, BaseQuerySetView):
    """Render options for a JAL widget, also used during rendering."""
