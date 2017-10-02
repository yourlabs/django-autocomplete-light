from dal import autocomplete

from django.conf.urls import url

from .models import TModel


urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(model=TModel),
        name='select2_fk',
    ),
]
