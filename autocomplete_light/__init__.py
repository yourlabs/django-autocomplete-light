"""
Provide tools to enable nice autocompletes in your Django project.
"""
from django import VERSION

if VERSION < (1, 9):
    from .shortcuts import *  # noqa
else:
    from .views import *  # noqa
    from .forms import *  # noqa

default_app_config = 'autocomplete_light.apps.AutocompleteLightConfig'
