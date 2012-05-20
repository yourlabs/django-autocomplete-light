"""
An url to ChannelView.

autocomplete_light_channel
    Given a 'channel' argument with the name of the channel, this url routes to
    ChannelView.
"""

from django.conf.urls.defaults import patterns, url
from django.views.decorators.csrf import csrf_exempt

from views import ChannelView

urlpatterns = patterns('',
    url(r'^channel/(?P<channel>[-\w]+)/$',
        csrf_exempt(ChannelView.as_view()),
        name='autocomplete_light_channel'
    ),
)
