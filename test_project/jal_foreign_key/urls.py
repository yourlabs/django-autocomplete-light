from dal import autocomplete

from django.conf.urls import url

from .models import TModel


urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.JalQuerySetView.as_view(model=TModel),
        name='jal_fk',
    ),
]
