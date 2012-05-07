from django.conf import settings
from django.core import urlresolvers

import autocomplete_light

def make_configuration(registry):
    configuration = {
        'registry': registry,
        'urls': {}
    }

    for name, channel_class in registry:
        configuration['urls'][name] = urlresolvers
