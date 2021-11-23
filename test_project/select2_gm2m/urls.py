from dal import autocomplete

from django.urls import re_path as url
from django.contrib.auth.models import Group
from django.views import generic

from .forms import TForm
from .models import TModel


urlpatterns = [
    url(
        '^select2_gm2m/$',
        autocomplete.Select2QuerySetSequenceView.as_view(
            queryset=autocomplete.QuerySetSequence(
                Group.objects.all(),
                TModel.objects.all(),
            )
        ),
        name='select2_gm2m',
    ),
    url(
        'test/(?P<pk>\d+)/$',
        generic.UpdateView.as_view(
            model=TModel,
            form_class=TForm,
        )
    ),
]
