from autocomplete_light.exceptions import AutocompleteNotRegistered
from django import http
from django.utils.encoding import force_text
from django.views import generic
from django.views.generic import base

__all__ = ['AutocompleteView', 'RegistryView', 'CreateView']


class GetRegistryMixin(object):
    def get_registry(self):
        if getattr(self, '_registry', None) is None:
            from autocomplete_light.registry import registry
            self._registry = registry
        return self._registry


class RegistryView(GetRegistryMixin, base.TemplateView):
    template_name = 'autocomplete_light/registry.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return http.HttpResponseForbidden()
        return super(RegistryView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return {
            'registry': self.get_registry(),
            'registry_items': self.get_registry().items(),
        }


class AutocompleteView(GetRegistryMixin, generic.View):
    """Simple view that routes the request to the appropriate autocomplete."""

    def get(self, request, *args, **kwargs):
        """
        Return an HttpResponse with the return value of
        autocomplete.autocomplete_html().

        This view is called by the autocomplete script, it is expected to
        return the rendered autocomplete box contents.

        To do so, it gets the autocomplete class from the registry, given the
        url keyword argument autocomplete, that should be the autocomplete
        name.

        Then, it instanciates the autocomplete with no argument as usual, and
        calls autocomplete.init_for_request, passing all arguments it recieved.

        Finnaly, it makes an HttpResponse with the result of
        autocomplete.autocomplete_html(). The javascript will use that to
        fill the autocomplete suggestion box.
        """
        try:
            autocomplete_class = self.get_registry()[kwargs['autocomplete']]
        except AutocompleteNotRegistered:
            return http.HttpResponseNotFound()
        autocomplete = autocomplete_class(request=request)
        return http.HttpResponse(autocomplete.autocomplete_html())

    def post(self, request, *args, **kwargs):
        """
        Just proxy autocomplete.post().

        This is the key to communication between the autocomplete and the
        widget in javascript. You can use it to create results and such.
        """
        autocomplete_class = self.get_registry()[kwargs['autocomplete']]
        autocomplete = autocomplete_class()
        return autocomplete.post(request, *args, **kwargs)


class CreateView(generic.CreateView):
    """Simple wrapper for generic.CreateView, that responds to _popup."""

    def is_popup(self):
        return self.request.GET.get('_popup', False)

    def respond_script(self, obj=None):
        if obj is None:
            obj = self.object

        html = []
        html.append('<script type="text/javascript">')
        html.append('opener.dismissAddAnotherPopup( window, "%s", "%s" );' % (
            force_text(obj.pk), force_text(obj).replace('"', '\\"')))
        html.append('</script>')

        html = ''.join(html)

        return http.HttpResponse(html, status=201)

    def form_valid(self, form):
        """ If request.GET._popup, return some javascript. """
        if self.is_popup():
            self.success_url = '/'  # avoid ImproperlyConfigured

        response = super(CreateView, self).form_valid(form)

        if not self.is_popup():
            return response

        return self.respond_script()
