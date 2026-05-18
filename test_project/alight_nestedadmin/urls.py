from django.urls import re_path as url

from dal import autocomplete

from .models import TModelThree


class LinkedDataView(autocomplete.AlightQuerySetView):
    def get_queryset(self):
        level_one = self.forwarded.get('level_one', None)
        level_two = self.forwarded.get('level_two', None)
        if not level_one or not level_two:
            raise Exception('Linked fields are not forwarded properly for nested admin')
        return TModelThree.objects.all()


urlpatterns = [
    url(
        '^linked_data/$',
        LinkedDataView.as_view(),
        name='nested_alight_linked_data',
    ),
]
