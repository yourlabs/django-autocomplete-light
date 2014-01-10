from django.conf.urls import patterns, url

urlpatterns = patterns('navigation_autocomplete.views',
    url(r'^$', 'navigation_autocomplete', name='navigation_autocomplete'),
)
