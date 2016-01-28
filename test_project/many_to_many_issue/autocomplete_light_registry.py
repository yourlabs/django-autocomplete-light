from autocomplete_light import shortcuts as al
from many.models import Cat


class CatAutocomplete(al.AutocompleteModelBase):
    search_fields = ['name', ]
    model = Cat


al.register(Cat, CatAutocomplete)

