from django import template

register = template.Library()

@register.filter
def autocomplete_light_result_as_html(result, channel):
    return channel.result_as_html(result)

@register.filter
def autocomplete_light_result_as_json(result, channel):
    return channel.result_as_json(result)
