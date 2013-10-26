from django.contrib import admin

import autocomplete_light

from models import MediaFilter, Media


class MediaFilterAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(MediaFilter)
admin.site.register(MediaFilter, MediaFilterAdmin)

admin.site.register(Media)
