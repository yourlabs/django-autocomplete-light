from cities_light.contrib.autocompletes import CityAutocomplete
from cities_light.models import City
from tagging.models import Tag

import autocomplete_light

class CityAutocompleteJSONP(autocomplete_light.AutocompleteModelJSONP):
    search_fields = ('search_names',)
    choices = City.objects.all()



autocomplete_light.register(CityAutocompleteJSONP)
