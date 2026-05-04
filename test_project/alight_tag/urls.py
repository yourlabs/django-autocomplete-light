from django.urls import re_path as url

from dal import autocomplete


TAGS = ['django', 'python', 'javascript', 'css']


class TagListView(autocomplete.AlightListView):
    def get_list(self):
        return TAGS

    def create(self, text):
        TAGS.append(text)
        return text


urlpatterns = [
    url(
        r'autocomplete/$',
        TagListView.as_view(),
        name='alight_tag',
    ),
]
