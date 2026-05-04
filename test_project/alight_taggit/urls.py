from django.urls import re_path as url
from taggit.models import Tag

from dal import autocomplete

urlpatterns = [
    url(
        r'test-autocomplete/$',
        autocomplete.AlightQuerySetView.as_view(queryset=Tag.objects.order_by('name')),
        name='alight_taggit',
    ),
]
