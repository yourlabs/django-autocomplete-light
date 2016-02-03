from dal import autocomplete

from django.conf.urls import url
from django.contrib.auth.models import Group
from django.views import generic

from .forms import TestForm
from .models import TestModel


urlpatterns = [
    url(
        '^select2-generic-m2m/$',
        autocomplete.Select2QuerySetSequenceView.as_view(
            queryset=autocomplete.QuerySetSequence(
                Group.objects.all(),
                TestModel.objects.all(),
            )
        ),
        name='select2_generic_m2m',
    ),
    url(
        'test/(?P<pk>\d+)/$',
        generic.UpdateView.as_view(
            model=TestModel,
            form_class=TestForm,
        )
    ),
]
