import autocomplete_light.shortcuts as autocomplete_light
from django import http

from .models import OnTheFly


class OnTheFlyAutocomplete(autocomplete_light.AutocompleteModelBase):
    choices = OnTheFly.objects.all()

    def autocomplete_html(self):
        html = super(OnTheFlyAutocomplete, self).autocomplete_html()
        html += '<span data-value="create">Create Fly</span>'
        return html

    def post(self, request, *args, **kwargs):
        return http.HttpResponse(
            OnTheFly.objects.create(name=request.POST['name']).pk
        )
autocomplete_light.register(OnTheFly, OnTheFlyAutocomplete)
