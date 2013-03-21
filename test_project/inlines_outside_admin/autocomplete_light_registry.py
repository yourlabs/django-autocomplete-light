import autocomplete_light

from models import OutsideAdmin

autocomplete_light.register(OutsideAdmin, search_fields=('name',))
