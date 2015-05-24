import autocomplete_light.shortcuts as al

from django import VERSION
from django.conf.urls import patterns, url
from django.views import generic

from .forms import NonAdminAddAnotherModelForm
from .models import NonAdminAddAnotherModel

urlpatterns = [
    url(r'$', al.CreateView.as_view(
        model=NonAdminAddAnotherModel, form_class=NonAdminAddAnotherModelForm),
        name='non_admin_add_another_model_create'),
    url(r'(?P<pk>\d+)/$', generic.UpdateView.as_view(
        model=NonAdminAddAnotherModel, form_class=NonAdminAddAnotherModelForm),
        name='non_admin_add_another_model_update'),
]

if VERSION < (1, 9):
    urlpatterns = patterns('', *urlpatterns)
