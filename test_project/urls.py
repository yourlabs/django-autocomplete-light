import views
from django.contrib import admin
from django.urls import include
from django.urls import re_path as url

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),

    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.LoginView.as_view()),

    url(r'^alight_foreign_key/', include('alight_foreign_key.urls')),
    url(r'^alight_many_to_many/', include('alight_many_to_many.urls')),
    url(r'^alight_linked_data/', include('alight_linked_data.urls')),
    url(r'^alight_list/', include('alight_list.urls')),
    url(r'^alight_tag/', include('alight_tag.urls')),
    url(r'^alight_one_to_one/', include('alight_one_to_one.urls')),
    url(r'^alight_forward_different_fields/', include('alight_forward_different_fields.urls')),  # noqa: E501
    url(r'^alight_rename_forward/', include('alight_rename_forward.urls')),
    url(r'^alight_secure_data/', include('alight_secure_data.urls')),
    url(r'^alight_outside_admin/', include('alight_outside_admin.urls')),
    url(r'^alight_taggit/', include('alight_taggit.urls')),
    url(r'^alight_generic_foreign_key/', include('alight_generic_foreign_key.urls')),
    url(r'^alight_nestedadmin/', include('alight_nestedadmin.urls')),
    url(r'^alight_djhacker_formfield/', include('alight_djhacker_formfield.urls')),

    url(r'^dal_single/', views.BasicDALView, name='isolated_dal_single'),
    url(r'^dal_multi/', views.BasicDALMultiView, name='isolated_dal_multi'),

    url(r'^secure_data/', include('select2_secure_data.urls')),
    url(r'^linked_data/', include('select2_linked_data.urls')),
    url(r'^rename_forward/', include('select2_rename_forward.urls')),
    url(r'^forward_different_fields/',
        include('select2_forward_different_fields.urls')),
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
