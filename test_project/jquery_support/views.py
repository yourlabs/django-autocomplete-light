# Create your views here.
from cities_light.contrib.autocompletes import CityAutocomplete
from django.views.generic.base import TemplateView

import autocomplete_light_registry

class JquerySupportView(TemplateView):
    template_name = 'jquery_support/index.html'
    pass
