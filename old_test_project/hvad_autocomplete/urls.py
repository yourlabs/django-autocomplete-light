from django.conf.urls import patterns, url
from django.views import generic

from forms import ItemForm
from models import Category, Item

urlpatterns = patterns('',
    url(r'item/add/$', generic.CreateView.as_view(
        model=Item, form_class=ItemForm)),
    url(r'item/(?P<pk>\d+)/update/$', generic.UpdateView.as_view(
        model=Item, form_class=ItemForm), name='item_update'),
)
