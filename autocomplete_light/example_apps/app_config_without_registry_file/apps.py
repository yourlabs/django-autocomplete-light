from django.apps import AppConfig

import autocomplete_light


class AppConfigWithoutRegistryAutocomplete(
    autocomplete_light.AutocompleteListBase):

    choices = ['a', 'b']


class AppConfigWithoutRegistryFile(AppConfig):
    name = 'autocomplete_light.example_apps.app_config_without_registry_file'

    def ready(self):
        autocomplete_light.register(AppConfigWithoutRegistryAutocomplete)
