from django.conf.urls import patterns, url

from views import FormsetView

urlpatterns = patterns('',
    url(r'$', FormsetView.as_view()),
)
