from django.conf.urls.defaults import *

from views import JsonChannelView

urlpatterns = patterns('',
    url(r'^channel/(?P<channel>[-\w]+)/$',
        JsonChannelView.as_view(),
        name='autocomplete_light_json_channel'
    ),
)

