from django.urls import re_path as url

from dal import autocomplete

from .models import TModel


class AlightLinkedDataView(autocomplete.AlightQuerySetView):
    def get_queryset(self):
        qs = super().get_queryset()
        owner = self.forwarded.get('owner', None)
        if owner:
            qs = qs.filter(owner_id=owner)
        return qs


urlpatterns = [
    url(
        r'test-autocomplete/$',
        AlightLinkedDataView.as_view(model=TModel),
        name='alight_linked_data',
    ),
]
