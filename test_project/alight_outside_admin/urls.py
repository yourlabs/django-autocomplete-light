from django.urls import re_path as url

from .views import UpdateView

urlpatterns = [
    url(
        r'^$',
        UpdateView.as_view(),
        name='alight_outside_admin',
    ),
]
