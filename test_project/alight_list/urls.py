from django.urls import re_path as url

from dal import autocomplete


class TModelListView(autocomplete.AlightListView):
    def get_list(self):
        return ['apple', 'mango', 'apricot', 'orange']

    def create(self, text):
        return text


class TModelGroupListView(autocomplete.AlightGroupListView):
    def get_list(self):
        return [
            ('Tropical', 'mango'),
            ('Tropical', 'papaya'),
            ('Temperate', 'apple'),
            ('Temperate', 'pear'),
        ]


urlpatterns = [
    url(
        r'autocomplete/$',
        TModelListView.as_view(),
        name='alight_list',
    ),
    url(
        r'group-autocomplete/$',
        TModelGroupListView.as_view(),
        name='alight_group_list',
    ),
]
