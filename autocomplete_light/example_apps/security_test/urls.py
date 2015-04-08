from django import VERSION
from django.conf.urls import patterns, url
from django.views import generic

from .forms import AutocompleteItemForm, DjangoItemForm
from .models import Item

urlpatterns = [
    url(r'autocomplete/(?P<pk>\d+)/', generic.UpdateView.as_view(
        form_class=AutocompleteItemForm,
        queryset=Item.objects.filter(private=False))),
    url(r'django/(?P<pk>\d+)/', generic.UpdateView.as_view(
        form_class=DjangoItemForm,
        queryset=Item.objects.filter(private=False))),
]

if VERSION < (1, 9):
    urlpatterns = patterns('', *urlpatterns)
