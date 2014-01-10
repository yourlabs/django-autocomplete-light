from django.conf.urls import patterns, url
from django.views import generic

import autocomplete_light

from .forms import NonAdminAddAnotherModelForm
from .models import NonAdminAddAnotherModel


urlpatterns = patterns('',
    url(r'$', autocomplete_light.CreateView.as_view(
        model=NonAdminAddAnotherModel, form_class=NonAdminAddAnotherModelForm),
        name='non_admin_add_another_model_create'),
    url(r'(?P<pk>\d+)/$', generic.UpdateView.as_view(
        model=NonAdminAddAnotherModel, form_class=NonAdminAddAnotherModelForm),
        name='non_admin_add_another_model_update'),
)
