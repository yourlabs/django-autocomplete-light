from django import http
from django.views import generic
from django.views.generic import base

import autocomplete_light

__all__ = ['AutocompleteView', 'RegistryView']


class RegistryView(base.TemplateView):
    template_name = 'autocomplete_light/registry.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return http.HttpResponseForbidden()
        return super(RegistryView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            'registry': autocomplete_light.registry,
        }


class AutocompleteView(generic.View):
    """Simple view that routes the request to the appropriate autocomplete."""

    def get(self, request, *args, **kwargs):
        """
        Return an HttpResponse with the return value of
        autocomplete.render_autocomplete().

        This view is called by the autocomplete script, it is expected to
        return the rendered autocomplete box contents.

        To do so, it gets the autocomplete class from the registry, given the
        url keyword argument autocomplete, that should be the autocomplete
        name.

        Then, it instanciates the autocomplete with no argument as usual, and
        calls autocomplete.init_for_request, passing all arguments it recieved.

        Finnaly, it makes an HttpResponse with the result of
        autocomplete.render_autocomplete(). The javascript will use that to
        fill the autocomplete suggestion box.
        """
        try:
            autocomplete_class = autocomplete_light.registry[
                kwargs['autocomplete']]
        except KeyError:
            return http.HttpResponseNotFound()
        autocomplete = autocomplete_class(request=request)
        return http.HttpResponse(autocomplete.autocomplete_html())

    def post(self, request, *args, **kwargs):
        """
        Just proxy autocomplete.post().

        This is the key to communication between the autocomplete and the
        widget in javascript. You can use it to create results and such.
        """
        autocomplete_class = autocomplete_light.registry[
            kwargs['autocomplete']]
        autocomplete = autocomplete_class()
        return autocomplete.post(request, *args, **kwargs)


class CreateView(generic.CreateView):
    def form_valid(self, form):
        response = super(CreateView, self).form_valid(form)

        if not self.request.GET.get('_popup', False):
            return response

        html = []
        html.append(u'<script type="text/javascript">')
        html.append(u'opener.dismissAddAnotherPopup( window, "%s", "%s" );' % (
            unicode(self.object.pk), unicode(self.object).replace('"', '\\"')))
        html.append(u'</script>')

        html = u''.join(html)

        return http.HttpResponse(html, status=201)
