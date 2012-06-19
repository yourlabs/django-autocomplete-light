"""
An url to AutocompleteView.

autocomplete_light_autocomplete
    Given a 'autocomplete' argument with the name of the autocomplete, this url
    routes to AutocompleteView.
"""

from django.conf.urls.defaults import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from views import AutocompleteView, RegistryView

urlpatterns = patterns('',
    url(r'^(?P<autocomplete>[-\w]+)/$',
        csrf_exempt(AutocompleteView.as_view()),
        name='autocomplete_light_autocomplete'
    ),
    url(r'^$',
        RegistryView.as_view(),
        name='autocomplete_light_registry'
    ),
)
