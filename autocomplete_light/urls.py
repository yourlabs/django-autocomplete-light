"""
An url to AutocompleteView.

autocomplete_light_autocomplete
    Given a 'autocomplete' argument with the name of the autocomplete, this url
    routes to AutocompleteView.

autocomplete_light_registry
    Renders the autocomplete registry, good for debugging, requires being
    authenticated as superuser.
"""

try:
    from django.conf.urls import patterns, url
except ImportError:
    # Django < 1.5
    from django.conf.urls.defaults import patterns, url

from django.views.generic.base import TemplateView

from .views import AutocompleteView, RegistryView


urlpatterns = patterns('',
    url(r'^(?P<autocomplete>[-\w]+)/$',
        AutocompleteView.as_view(),
        name='autocomplete_light_autocomplete'
    ),
    url(r'^$',
        RegistryView.as_view(),
        name='autocomplete_light_registry'
    ),
)
