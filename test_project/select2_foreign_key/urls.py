from dal import autocomplete

try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

from .models import TModel


urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(model=TModel),
        name='select2_fk',
    ),
]
