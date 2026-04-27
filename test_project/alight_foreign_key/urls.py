from dal import autocomplete
from django.urls import re_path as url
from .models import TModel


urlpatterns = [
    url(
        r'test-autocomplete/$',
        autocomplete.AlightQuerySetView.as_view(model=TModel),
        name='alight_fk',
    ),
]
