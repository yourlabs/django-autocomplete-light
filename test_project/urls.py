import views
from django.contrib import admin
from django.urls import include
from django.urls import re_path as url

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),

    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.LoginView.as_view()),

    url(r'^dal_single/', views.BasicDALView, name='isolated_dal_single'),
    url(r'^dal_multi/', views.BasicDALMultiView, name='isolated_dal_multi'),

    url(r'^secure_data/', include('secure_data.urls')),
    url(r'^linked_data/', include('linked_data.urls')),
    url(r'^rename_forward/', include('rename_forward.urls')),
    url(r'^forward_different_fields/',
        include('forward_different_fields.urls')),
    url(r'^select2_nestedadmin/', include('select2_nestedadmin.urls')),

    url(r'^select2_foreign_key/', include('select2_foreign_key.urls')),
    url(r'^select2_list/', include('select2_list.urls')),
    url(r'^select2_generic_foreign_key/',
        include('select2_generic_foreign_key.urls')),
    url(r'^select2_many_to_many/',
        include('select2_many_to_many.urls')),
    url(r'^select2_one_to_one/', include('select2_one_to_one.urls')),

    url(r'^select2_outside_admin/', include('select2_outside_admin.urls')),
    url(r'^select2_taggit/', include('select2_taggit.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^select2_djhacker_formfield/', include('select2_djhacker_formfield.urls')),
]
