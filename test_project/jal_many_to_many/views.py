from dal import autocomplete

from .models import TModel


class AutocompleteView(autocomplete.JalQuerySetView):
    model = TModel
