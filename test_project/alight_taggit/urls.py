from django.urls import re_path as url
from taggit.models import Tag

from dal import autocomplete

urlpatterns = [
    url(
        r'test-autocomplete/$',
        autocomplete.AlightTagAutocompleteView.as_view(
            queryset=Tag.objects.order_by('name'),
            create_field='name',
        ),
        name='alight_taggit',
    ),
]
