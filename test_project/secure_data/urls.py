from dal import autocomplete

from django.conf.urls import url

from .models import TestModel


class SecureDataView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return TestModel.objects.filter(owner=self.request.user)


urlpatterns = [
    url(
        '^secure-data/$',
        SecureDataView.as_view(),
        name='secure_data',
    ),
]
