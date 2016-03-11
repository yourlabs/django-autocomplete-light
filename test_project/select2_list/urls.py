import json

from dal import autocomplete

from django.conf.urls import url
from django import http
from django.views import generic


class YourListView(autocomplete.ViewMixin, generic.View):
    def get(self, request, *args, **kwargs):
        results = ['windows', 'linux']

        if self.q:
            results = [
                x for x in results if self.q in x
            ]
        return http.HttpResponse(json.dumps({
            'results': [dict(id=x, text=x) for x in results]
        }))


urlpatterns = [
    url(
        'test-autocomplete/$',
        YourListView.as_view(),
        name='select2_list',
    ),
]
