from django.urls import re_path as url

from .views import SecureDataView

urlpatterns = [
    url(
        '^autocomplete/$',
        SecureDataView.as_view(),
        name='alight_secure_data_autocomplete',
    ),
]
