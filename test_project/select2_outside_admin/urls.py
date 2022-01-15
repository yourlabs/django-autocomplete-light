try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

from .views import UpdateView


urlpatterns = [
    url(
        r'^$',
        UpdateView.as_view(),
        name='select2_outside_admin',
    ),
]
