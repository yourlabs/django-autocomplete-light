from django import http
from django.views import generic

import autocomplete_light

__all__ = ['JsonChannelView']

class JsonChannelView(generic.View):
    def get(self, request, *args, **kwargs):
        channel_class = autocomplete_light.registry[kwargs['channel']]
        channel = channel_class()
        channel.init_for_request(request, *args, **kwargs)
        return http.HttpResponse(channel.render_autocomplete())

