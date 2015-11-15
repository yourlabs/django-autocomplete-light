import autocomplete_light.shortcuts as al

from autocomplete_light.compat import url, urls
from django.views import generic

from .forms import NonAdminAddAnotherModelForm
from .models import NonAdminAddAnotherModel

urlpatterns = urls([
    url(r'$', al.CreateView.as_view(
        model=NonAdminAddAnotherModel, form_class=NonAdminAddAnotherModelForm),
        name='non_admin_add_another_model_create'),
    url(r'(?P<pk>\d+)/$', generic.UpdateView.as_view(
        model=NonAdminAddAnotherModel, form_class=NonAdminAddAnotherModelForm),
        name='non_admin_add_another_model_update'),
])
