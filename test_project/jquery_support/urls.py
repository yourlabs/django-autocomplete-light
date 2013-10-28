from django.conf.urls import patterns, url
from jquery_support.views import JquerySupportView


urlpatterns = patterns('',
    url(r'$', JquerySupportView.as_view()),
)
