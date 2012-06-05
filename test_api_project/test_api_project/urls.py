from django.conf.urls import patterns, include, url

import autocomplete_light
autocomplete_light.autodiscover()
import autocomplete_light_registry

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_api_project.views.home', name='home'),
    # url(r'^test_api_project/', include('test_api_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^cities_light/', include('cities_light.contrib.restframework')),
)
