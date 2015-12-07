import autocomplete_light.shortcuts as autocomplete_light
from django import http

from .models import OnTheFly


class OnTheFlyAutocomplete(autocomplete_light.AutocompleteModelBase):
    choices = OnTheFly.objects.all()

    def autocomplete_html(self):
        html = super(OnTheFlyAutocomplete, self).autocomplete_html()

        q = self.request.REQUEST.get('q')
        if q and not self.choices.filter(name=q).exists():
            html += '<span data-value="create">Create "{}"</span>'.format(q)
        return html

    def post(self, request, *args, **kwargs):
        return http.HttpResponse(
            OnTheFly.objects.create(name=request.POST['name']).pk
        )
autocomplete_light.register(OnTheFly, OnTheFlyAutocomplete)
