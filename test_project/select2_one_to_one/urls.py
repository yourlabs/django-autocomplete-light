from dal import autocomplete

from django.urls import re_path as url
from django.views import generic

from .forms import TForm
from .models import TModel


urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=TModel,
            create_field='name',
        ),
        name='select2_one_to_one_autocomplete',
    ),
    url(
        'test/(?P<pk>\d+)/$',
        generic.UpdateView.as_view(
            model=TModel,
            form_class=TForm,
        )
    ),
]
