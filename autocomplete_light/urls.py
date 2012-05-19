from django.conf.urls.defaults import *
from django.views.decorators.csrf import csrf_exempt

from views import ChannelView

urlpatterns = patterns('',
    url(r'^channel/(?P<channel>[-\w]+)/$',
        csrf_exempt(ChannelView.as_view()),
        name='autocomplete_light_channel'
    ),
)
