from dal import autocomplete


class CustomAutocomplete(autocomplete.Select2QuerySetView):
    """Overriding the Autocomplete class"""

    def has_add_permission(self, request):
        return True
