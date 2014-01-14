from django.conf.urls import patterns, url
from views import TaggitDemoCreate

urlpatterns = patterns('',
     url(r'^create/$', TaggitDemoCreate.as_view()),
)

