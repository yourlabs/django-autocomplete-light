from django.urls import re_path as url
from taggit.models import Tag

from dal import autocomplete


class TagNameView(autocomplete.AlightQuerySetView):
    def get_result_value(self, result):
        return result.name


urlpatterns = [
    url(
        r'test-autocomplete/$',
        TagNameView.as_view(queryset=Tag.objects.order_by('name')),
        name='alight_taggit',
    ),
]
