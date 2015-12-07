from django.conf.urls import url

from autocomplete_light.compat import url, urls
from .views import navigation_autocomplete

urlpatterns = urls([
    url(r'^$', navigation_autocomplete, name='navigation_autocomplete'),
])
