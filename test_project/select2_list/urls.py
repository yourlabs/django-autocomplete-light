from django.conf.urls import url

from .views import Select2ListViewAutocomplete


urlpatterns = [
    url(
        'test-autocomplete/$',
        Select2ListViewAutocomplete.as_view(),
        name='select2_list',
    ),
]
