from django.contrib import admin
from django.urls import include, re_path as url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^component-test/$', views.component_test, name='component_test'),
    url(r'^admin/', admin.site.urls),

    url(r'^fk/', include('alight_foreign_key.urls')),
    url(r'^fk/new/$', views.FKCreateView.as_view(), name='fk_create'),
    url(r'^fk/(?P<pk>\d+)/$', views.FKUpdateView.as_view(), name='fk_update'),

    url(r'^m2m/', include('alight_many_to_many.urls')),
    url(r'^m2m/new/$', views.M2MCreateView.as_view(), name='m2m_create'),
    url(r'^m2m/(?P<pk>\d+)/$', views.M2MUpdateView.as_view(), name='m2m_update'),

    url(r'^linked/', include('alight_linked_data.urls')),
    url(r'^linked/new/$', views.LinkedCreateView.as_view(), name='linked_create'),
    url(r'^linked/(?P<pk>\d+)/$', views.LinkedUpdateView.as_view(), name='linked_update'),

    url(r'^list/', include('alight_list.urls')),
    url(r'^list/new/$', views.ListCreateView.as_view(), name='list_create'),
    url(r'^list/(?P<pk>\d+)/$', views.ListUpdateView.as_view(), name='list_update'),

    url(r'^tag/', include('alight_tag.urls')),
    url(r'^tag/new/$', views.TagCreateView.as_view(), name='tag_create'),
    url(r'^tag/(?P<pk>\d+)/$', views.TagUpdateView.as_view(), name='tag_update'),
]
