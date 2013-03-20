from autocomplete_light.contrib.hvad import AutocompleteModelBase
import autocomplete_light
from .models import Category


autocomplete_light.register(Category, AutocompleteModelBase,
                            search_fields=('name',))
