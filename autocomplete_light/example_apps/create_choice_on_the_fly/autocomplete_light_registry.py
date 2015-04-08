import autocomplete_light.shortcuts as autocomplete_light
from django import http

from .models import Fly


class FlyAutocomplete(autocomplete_light.AutocompleteModelBase):
    choices = Fly.objects.all()

    def autocomplete_html(self):
        html = super(FlyAutocomplete, self).autocomplete_html()
        html += '<span data-value="create">Create Fly</span>'
        return html

    def post(self, request, *args, **kwargs):
        return http.HttpResponse(
            Fly.objects.create(name=request.POST['name']).pk
        )
autocomplete_light.register(Fly, FlyAutocomplete)
