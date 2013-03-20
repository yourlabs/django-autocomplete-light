from autocomplete_light.contrib.hvad import AutocompleteModelBase
import autocomplete_light
from .models import Category

autocomplete_light.registry.autocomplete_model_base = AutocompleteModelBase

autocomplete_light.register(Category,
                            search_fields=('name',))
