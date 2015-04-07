from django.apps import AppConfig


class AutocompleteLightConfig(AppConfig):
    name = 'autocomplete_light'

    def ready(self):
        from autocomplete_light.registry import autodiscover
        autodiscover()
