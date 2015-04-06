from django.apps import AppConfig


class AppConfigWithoutRegistryFile(AppConfig):
    name = 'autocomplete_light.example_apps.app_config_without_registry_file'

    def ready(self):
        import autocomplete_light.shortcuts as autocomplete_light

        class AppConfigWithoutRegistryAutocomplete(
            autocomplete_light.AutocompleteListBase):
        
            choices = ['a', 'b']

        autocomplete_light.register(AppConfigWithoutRegistryAutocomplete)
