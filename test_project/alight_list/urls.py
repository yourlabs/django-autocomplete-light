from django.urls import re_path as url

from dal import autocomplete

from .models import TModel


class TModelListView(autocomplete.AlightListView):
    def get_list(self):
        return list(
            TModel.objects.exclude(test__isnull=True)
            .exclude(test='')
            .values_list('test', flat=True)
            .distinct()
        )

    def create(self, text):
        return text


urlpatterns = [
    url(
        r'autocomplete/$',
        TModelListView.as_view(),
        name='alight_list',
    ),
]
