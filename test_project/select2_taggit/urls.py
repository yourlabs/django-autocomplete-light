from django.urls import re_path as url
from taggit.models import Tag

from dal import autocomplete

urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            queryset=Tag.objects.order_by('name'),
        ),
        name='select2_taggit',
    ),
]
