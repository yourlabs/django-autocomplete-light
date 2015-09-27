"""
Provide tools to enable nice autocompletes in your Django project.
"""
import django

if django.VERSION < (1, 9):
    from .shortcuts import *  # noqa
else:
    from .views import *  # noqa
    from .forms import *  # noqa

default_app_config = 'autocomplete_light.apps.AutocompleteLightConfig'

__version__ = (2, 2, 8)
