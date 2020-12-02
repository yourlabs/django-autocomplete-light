from django.conf.urls import url

from .views import Select2ListViewAutocomplete, Select2ProvidedValueListViewAutocomplete


urlpatterns = [
    url(
        'test-autocomplete/$',
        Select2ListViewAutocomplete.as_view(),
        name='select2_list',
    ),
    url(
        'test-provided-value-autocomplete/$',
        Select2ProvidedValueListViewAutocomplete.as_view(),
        name='select2_povided_value_list',
    ),
]
