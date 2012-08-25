import autocomplete_light

from models import City

autocomplete_light.register(City, search_fields=("city",))

