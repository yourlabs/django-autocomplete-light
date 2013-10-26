from django.conf.urls import patterns, include, url
from django.views import generic

from models import TemplatedChoice


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', generic.DetailView.as_view(model=TemplatedChoice),
        name='templated_choice_detail'),
)
