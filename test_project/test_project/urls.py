from django.conf.urls import patterns, include, url
from django.views import generic

import autocomplete_light
autocomplete_light.autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_project.views.home', name='home'),
    # url(r'^test_project/', include('test_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'support_sandino/', include('support_sandino.urls')),
    url(r'^non_admin/', include('non_admin.urls', namespace='non_admin')),
    url(r'^non_admin_add_another/', include('non_admin_add_another.urls',
        namespace='non_admin_add_another')),
    url(r'^double_loading/', generic.TemplateView.as_view(
        template_name='double_loading.html')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^navigation/', include('navigation_autocomplete.urls')),
    url(r'^cities_light/', include('cities_light.contrib.restframework')),
)
