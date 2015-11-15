from django import VERSION
from autocomplete_light.compat import urls, url


urlpatterns = urls([
    url(r'^$', 'navigation_autocomplete', name='navigation_autocomplete'),
])
