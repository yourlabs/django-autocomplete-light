from dal import autocomplete

from django.conf.urls import url

from .models import TestModel


urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(model=TestModel),
        name='select2_fk',
    ),
]
