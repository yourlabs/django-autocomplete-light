from django.urls import re_path as url

from dal import autocomplete


FRUITS = ['apple', 'apricot', 'banana', 'cherry']


class FruitListView(autocomplete.AlightListView):
    def get_list(self):
        return FRUITS

    def create(self, text):
        FRUITS.append(text)
        return text


urlpatterns = [
    url(
        r'autocomplete/$',
        FruitListView.as_view(),
        name='alight_list',
    ),
]
