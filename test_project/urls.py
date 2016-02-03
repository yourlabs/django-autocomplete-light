import django

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^secure_data/', include('secure_data.urls')),
    url(r'^linked_data/', include('linked_data.urls')),

    url(r'^select2_foreign_key/', include('select2_foreign_key.urls')),
    url(r'^select2_generic_foreign_key/',
        include('select2_generic_foreign_key.urls')),
    url(r'^select2_generic_m2m/', include('select2_generic_m2m.urls')),
    url(r'^select2_many_to_many/',
        include('select2_many_to_many.urls')),
    url(r'^select2_one_to_one/', include('select2_one_to_one.urls')),
    url(r'^select2_taggit/', include('select2_taggit.urls')),
    url(r'^select2_tagulous/', include('select2_tagulous.urls')),
]

if django.VERSION < (1, 10):
    urlpatterns += [
        url(r'^select2_gm2m/', include('select2_gm2m.urls')),
    ]
