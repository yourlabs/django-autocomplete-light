from django.conf.urls.defaults import *

from views import ChannelView

urlpatterns = patterns('',
    url(r'^channel/(?P<channel>[-\w]+)/$',
        ChannelView.as_view(),
        name='autocomplete_light_channel'
    ),
)

