from dal import autocomplete

from django.urls import re_path as url

from .models import TModelThree


class NestedAdminError(Exception):
    pass


class LinkedDataView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # We don't really care about filtering in this test app, but only that
        # the values are forwarded properly.
        level_one = self.forwarded.get('level_one', None)
        level_two = self.forwarded.get('level_two', None)

        if not level_one or not level_two:
            raise NestedAdminError(
                'Linked fields are not forwarded properly for nested admin')

        return super(LinkedDataView, self).get_queryset()


urlpatterns = [
    url(
        '^linked_data/$',
        LinkedDataView.as_view(model=TModelThree),
        name='nested_linked_data'
    ),
]
