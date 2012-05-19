import autocomplete_light

from cities_light.contrib.autocomplete_light_restframework import RemoteCountryChannel, RemoteCityChannel
from cities_light.models import City, Country

class RemoteCountryChannel(RemoteCountryChannel):
    source_url = 'http://localhost:8000/cities_light/country/'

class RemoteCityChannel(RemoteCityChannel):
    source_url = 'http://localhost:8000/cities_light/city/'

autocomplete_light.register(Country, RemoteCountryChannel)
autocomplete_light.register(City, RemoteCityChannel)
