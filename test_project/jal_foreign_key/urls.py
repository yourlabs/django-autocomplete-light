from dal import autocomplete

from django.conf.urls import url

from .models import TestModel


urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.JalQuerySetView.as_view(model=TestModel),
        name='jal_fk',
    ),
]
