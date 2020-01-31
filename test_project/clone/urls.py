from django.conf.urls import url

from .views import UpdateView


urlpatterns = [
    url(
        r'^$',
        UpdateView.as_view(),
        name='clone',
    ),
]
