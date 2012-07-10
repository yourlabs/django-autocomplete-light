from cities_light.contrib.autocompletes import *

import autocomplete_light


autocomplete_light.register(Country, CountryRestAutocomplete,
    source_url='http://localhost:8000/cities_light/country/')

autocomplete_light.register(Region, RegionRestAutocomplete,
    source_url='http://localhost:8000/cities_light/region/')

autocomplete_light.register(City, CityRestAutocomplete,
    source_url='http://localhost:8000/cities_light/city/')
