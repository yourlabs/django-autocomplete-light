"""
An url to AutocompleteView.

autocomplete_light_autocomplete
    Given a 'autocomplete' argument with the name of the autocomplete, this url
    routes to AutocompleteView.

autocomplete_light_registry
    Renders the autocomplete registry, good for debugging, requires being
    authenticated as superuser.
"""
from django import VERSION

from .views import AutocompleteView, RegistryView

try:
    from django.conf.urls import patterns, url
except ImportError:
    # Django < 1.5
    from django.conf.urls.defaults import patterns, url

urlpatterns = [
    url(r'^(?P<autocomplete>[-\w]+)/$',
        AutocompleteView.as_view(),
        name='autocomplete_light_autocomplete'
    ),
    url(r'^$',
        RegistryView.as_view(),
        name='autocomplete_light_registry'
    ),
]

if VERSION < (1, 9):
    urlpatterns = patterns('', *urlpatterns)
