import six

from django.apps import AppConfig
from django.core import checks


class AutocompleteLightConfig(AppConfig):
    name = 'autocomplete_light'

    def ready(self):
        from autocomplete_light.registry import autodiscover
        autodiscover()
