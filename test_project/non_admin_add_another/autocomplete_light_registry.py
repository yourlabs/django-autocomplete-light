from django.core import urlresolvers

import autocomplete_light

from models import Widget


autocomplete_light.register(Widget, add_another_url_name='widget_create')
