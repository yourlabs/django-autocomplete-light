from django import template

register = template.Library()


@register.filter
def autocomplete_light_result_as_html(result, channel):
    """Return channel.result_as_html for result and channel."""
    return channel.result_as_html(result)
