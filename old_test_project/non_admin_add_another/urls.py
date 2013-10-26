from django.conf.urls import patterns, url
from django.views import generic

import autocomplete_light

from forms import WidgetForm
from models import Widget


urlpatterns = patterns('',
    url(r'widget/add/$', autocomplete_light.CreateView.as_view(
        model=Widget, form_class=WidgetForm), name='widget_create'),
    url(r'widget/(?P<pk>\d+)/update/$', generic.UpdateView.as_view(
        model=Widget, form_class=WidgetForm), name='widget_update'),
)
