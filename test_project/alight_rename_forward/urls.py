from django.urls import re_path as url

from dal import autocomplete

from .models import TModel


class LinkedDataView(autocomplete.AlightQuerySetView):
    def get_queryset(self):
        qs = TModel.objects.all()

        if self.forwarded.get('secret') != 42:
            return qs.none()

        possessor = self.forwarded.get('possessor', None)
        if possessor:
            qs = qs.filter(owner_id=possessor)

        return qs


urlpatterns = [
    url(
        '^autocomplete/$',
        LinkedDataView.as_view(),
        name='alight_rename_forward_autocomplete',
    ),
]
