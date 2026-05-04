from django.urls import re_path as url

from dal import autocomplete

from .models import TModel


class AlightLinkedDataView(autocomplete.AlightQuerySetView):
    def get_queryset(self):
        qs = super().get_queryset()
        group = self.forwarded.get('group', None)
        if group:
            qs = qs.filter(group_id=group)
        return qs


urlpatterns = [
    url(
        r'test-autocomplete/$',
        AlightLinkedDataView.as_view(model=TModel),
        name='alight_linked_data',
    ),
]
