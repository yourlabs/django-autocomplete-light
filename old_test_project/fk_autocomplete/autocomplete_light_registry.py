import autocomplete_light

from cities_light.models import City

autocomplete_light.register(City, search_fields=('search_names',),
    autocomplete_js_attributes={'placeholder': 'city name ..'})
