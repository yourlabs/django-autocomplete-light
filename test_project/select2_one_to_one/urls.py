from dal import autocomplete

from django.conf.urls import url
from django.views import generic

from .forms import TestForm
from .models import TestModel


urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(
            model=TestModel,
            create_field='name',
        ),
        name='select2_one_to_one_autocomplete',
    ),
    url(
        'test/(?P<pk>\d+)/$',
        generic.UpdateView.as_view(
            model=TestModel,
            form_class=TestForm,
        )
    ),
]
