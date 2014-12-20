import autocomplete_light


class AppConfigWithRegistryAutocomplete(
    autocomplete_light.AutocompleteListBase):

    choices = ['a', 'b']
autocomplete_light.register(AppConfigWithRegistryAutocomplete)
