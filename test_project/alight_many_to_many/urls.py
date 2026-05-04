from django.urls import re_path as url

from dal import autocomplete

from .models import TModel

urlpatterns = [
    url(
        r'test-autocomplete/$',
        autocomplete.AlightQuerySetView.as_view(model=TModel, create_field='name'),
        name='alight_m2m',
    ),
]
