from django.apps import AppConfig

import autocomplete_light


class AutocompleteLightConfig(AppConfig):
    name = 'autocomplete_light'

    def ready(self):
        autocomplete_light.autodiscover()
