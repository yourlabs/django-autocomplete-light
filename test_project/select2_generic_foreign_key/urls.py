# from dal import autocomplete

from django.conf.urls import url
# from django.contrib.auth.models import Group
from django.views import generic

from .forms import TForm
from .models import TModel


urlpatterns = [
    url(
        'test/(?P<pk>\d+)/$',
        generic.UpdateView.as_view(
            model=TModel,
            form_class=TForm,
        )
    ),
]
urlpatterns.extend(TForm.as_urls())
