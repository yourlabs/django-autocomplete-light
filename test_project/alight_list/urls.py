from django.urls import re_path as url

from dal import autocomplete


class TModelListView(autocomplete.AlightListView):
    def get_list(self):
        return ['apple', 'grape', 'apricot', 'orange']

    def create(self, text):
        return text


urlpatterns = [
    url(
        r'autocomplete/$',
        TModelListView.as_view(),
        name='alight_list',
    ),
]
