from cities_light.models import City, Country
import autocomplete_light


class AutocompletePeople(autocomplete_light.AutocompleteGenericBase):
    choices = (
        City.objects.all(),
        Country.objects.all(),
    )

    search_fields = (
        ('search_names',),
        ('name',)
    )

    autocomplete_js_attributes = {'placeholder': 'suggestions...', 'minimum_characters': 0}
autocomplete_light.register(AutocompletePeople)
