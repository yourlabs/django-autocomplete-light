from __future__ import unicode_literals

from django import template
from django.utils import safestring

register = template.Library()


@register.filter
def autocomplete_light_data_attributes(attributes, prefix=''):
    html = []

    for key, value in attributes.items():
        html.append('data-%s%s="%s"' % (prefix, key.replace('_', '-'), value))

    return safestring.mark_safe(' '.join(html))


@register.filter
def autocomplete_light_choice_html(choice, autocomplete):
    """Return autocomplete.choice_html(choice)"""
    return safestring.mark_safe(autocomplete.choice_html(choice))
