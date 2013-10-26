from django.contrib import admin

import autocomplete_light

from models import Creatable


class CreatableAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Creatable)
admin.site.register(Creatable, CreatableAdmin)
