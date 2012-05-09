from django import template
from django.conf import settings

import autocomplete_light

register = template.Library()

@register.simple_tag
def autocomplete_light_js(include_autocomplete=True, include_deck=True):
    output = ''
    if include_autocomplete:
        output += '<script src="%sautocomplete_light/autocomplete.js" type="text/javascript"></script>' % settings.STATIC_URL
    if include_deck:
        output += '<script src="%sautocomplete_light/deck.js" type="text/javascript"></script>' % settings.STATIC_URL
        
    for js in autocomplete_light.jslist:
        output += '<script src="%s%s" type="text/javascript"></script>' % (
            settings.STATIC_URL, js)
    return output

@register.filter
def autocomplete_light_result_as_html(result, channel):
    return channel.result_as_html(result)

@register.filter
def autocomplete_light_result_as_json(result, channel):
    return channel.result_as_json(result)
