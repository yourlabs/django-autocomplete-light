from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        'test-autocomplete/$',
        views.AutocompleteView.as_view(),
        name='jal_m2m',
    ),
]
