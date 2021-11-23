from dal import autocomplete

from django.urls import re_path as url

from .models import TModel


class SecureDataView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return TModel.objects.filter(owner=self.request.user)


urlpatterns = [
    url(
        '^secure-data/$',
        SecureDataView.as_view(),
        name='secure_data',
    ),
]
