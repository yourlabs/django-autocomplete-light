from django import VERSION
from django.views import generic

from autocomplete_light.compat import url, urls
from .forms import AutocompleteItemForm, DjangoItemForm
from .models import Item

urlpatterns = urls([
    url(r'autocomplete/(?P<pk>\d+)/', generic.UpdateView.as_view(
        form_class=AutocompleteItemForm,
        queryset=Item.objects.filter(private=False))),
    url(r'django/(?P<pk>\d+)/', generic.UpdateView.as_view(
        form_class=DjangoItemForm,
        queryset=Item.objects.filter(private=False))),
])
