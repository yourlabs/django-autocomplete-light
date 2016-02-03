from dal import autocomplete

from django.conf.urls import url

from .models import TestModel


class LinkedDataView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = super(LinkedDataView, self).get_queryset()
        owner = self.forwarded.get('owner', None)

        if owner:
            qs = qs.filter(owner_id=owner)

        return qs


urlpatterns = [
    url(
        '^linked_data/$',
        LinkedDataView.as_view(model=TestModel),
        name='linked_data'
    ),
]
