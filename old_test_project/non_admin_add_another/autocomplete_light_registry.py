from django.core import urlresolvers

import autocomplete_light

from models import Widget


autocomplete_light.register(Widget, add_another_url_name='non_admin_add_another:widget_create')
