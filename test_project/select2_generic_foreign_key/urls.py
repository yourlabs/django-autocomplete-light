# from dal import autocomplete

try:
    from django.urls import re_path as url
except ImportError:
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
