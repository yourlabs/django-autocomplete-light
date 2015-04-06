from django.conf.urls import patterns, url

from .views import navigation_autocomplete

urlpatterns = [
    url(r'^$', navigation_autocomplete, name='navigation_autocomplete'),
]
