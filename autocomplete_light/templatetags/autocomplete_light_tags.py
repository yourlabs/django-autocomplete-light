from django import template
from django.conf import settings

import autocomplete_light

register = template.Library()


@register.simple_tag
def autocomplete_light_static(include_autocomplete=True, include_deck=True,
    include_style=True):
    """
    Render static_files that were autodiscovered, as well as javascript and
    css dependencies (optionnal).
    """

    static_list = []

    if include_autocomplete:
        static_list.append('autocomplete_light/autocomplete.js')
    if include_deck:
        static_list.append('autocomplete_light/deck.js')
    if include_style:
        static_list.append('autocomplete_light/style.css')

    static_list += autocomplete_light.registry.static_list

    output = ''
    for file in static_list:
        if file[-3:] == '.js':
            output += '''
                <script src="%s%s" type="text/javascript"></script>
                '''.strip() % (settings.STATIC_URL, file)
        elif file[-4:] == '.css':
            output += '''
                <link rel="stylesheet" type="text/css" href="%s%s"/>
                '''.strip() % (settings.STATIC_URL, file)

    return output


@register.filter
def autocomplete_light_result_as_html(result, channel):
    """Return channel.result_as_html for result and channel."""
    return channel.result_as_html(result)
