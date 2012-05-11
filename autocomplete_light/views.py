from django import http
from django.views import generic

import autocomplete_light

__all__ = ['ChannelView']


class ChannelView(generic.View):
    """Simple view that routes the request to the appropriate channel."""

    def get(self, request, *args, **kwargs):
        """
        Return an HttpResponse with the return value of
        channel.render_autocomplete().

        This view is called by the autocomplete script, it is expected to
        return the rendered autocomplete box contents.

        To do so, it gets the channel class from the registry, given the url
        keyword argument channel, that should be the channel name.

        Then, it instanciates the channel with no argument as usual, and calls
        channel.init_for_request, passing all arguments it recieved.

        Finnaly, it makes an HttpResponse with the result of
        channel.render_autocomplete(). The javascript will use that to fill the
        autocomplete suggestion box.
        """
        channel_class = autocomplete_light.registry[kwargs['channel']]
        channel = channel_class()
        channel.init_for_request(request, *args, **kwargs)
        return http.HttpResponse(channel.render_autocomplete())
