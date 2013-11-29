from django.conf.urls import url, patterns

from django.views import generic

from .models import Item
from .forms import DjangoItemForm, AutocompleteItemForm


urlpatterns = patterns('',
    url(r'autocomplete/(?P<pk>\d+)/', generic.UpdateView.as_view(
        form_class=AutocompleteItemForm,
        queryset=Item.objects.filter(private=False))),
    url(r'django/(?P<pk>\d+)/', generic.UpdateView.as_view(
        form_class=DjangoItemForm,
        queryset=Item.objects.filter(private=False))),
)
