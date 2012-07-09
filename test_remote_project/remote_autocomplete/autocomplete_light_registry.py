from cities_light.contrib.autocompletes import CityRestAutocomplete
from cities_light.models import City

import autocomplete_light


autocomplete_light.register(City, CityRestAutocomplete,
    source_url='http://localhost:8000/cities_light/city/')
