import autocomplete_light

from models import Media

autocomplete_light.register(Media, search_fields=('name',))
