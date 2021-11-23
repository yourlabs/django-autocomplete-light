from dal import autocomplete

from django.urls import re_path as url

from tagging.models import Tag


urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            queryset=Tag.objects.all(),
        ),
        name='select2_tagging',
    ),
]
