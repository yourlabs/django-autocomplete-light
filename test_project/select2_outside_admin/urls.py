from django.conf.urls import url

from .views import UpdateView
from select2_many_to_many import models


urlpatterns = [
    url(
        r'/$',
        UpdateView.as_view(),
        name='select2_outside_admin',
    ),
]
