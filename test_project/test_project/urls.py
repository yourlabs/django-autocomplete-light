import django

from django.conf.urls import patterns, include, url
from django.views import generic

if django.VERSION < (1, 7):
    import autocomplete_light
    autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

try:
    from hvad_autocomplete import urls as hvad
except ImportError:
    # django 1.6 not support by hvad
    hvad = None

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^navigation/', include('navigation_autocomplete.urls')),
    url(r'^security_test/',
        include('autocomplete_light.example_apps.security_test.urls')),
    url(r'^non_admin_add_another/',
        include('autocomplete_light.example_apps.non_admin_add_another.urls')),
    (r'^favicon.ico', generic.RedirectView.as_view(url='http://mozilla.org/favicon.ico')),
    (r'^$', generic.TemplateView.as_view(template_name='index.html'))
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
