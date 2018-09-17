import django
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view()),

    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.LoginView.as_view()),

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
]

if django.VERSION < (2, 0, 0):
    # pending upstream support
    urlpatterns += [
        url(r'^select2_tagging/', include('select2_tagging.urls')),
        url(r'^select2_gm2m/', include('select2_gm2m.urls')),
        url(r'^select2_generic_m2m/', include('select2_generic_m2m.urls')),
    ]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)), ]
