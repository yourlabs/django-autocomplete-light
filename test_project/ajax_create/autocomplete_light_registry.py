from django import http

import autocomplete_light

from models import Creatable


class AutocompleteCreatable(autocomplete_light.AutocompleteModelTemplate):
    autocomplete_template = 'ajax_create/autocomplete.html'

    def post(self, request, *args, **kwargs):
        choice = Creatable.objects.create(name=request.POST['createChoice'])
        return http.HttpResponse(self.choice_html(choice))


autocomplete_light.register(Creatable, AutocompleteCreatable)
