from django.contrib import admin

import autocomplete_light

from models import ItemModel, CodeModel

class ItemModelAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(ItemModel)

admin.site.register(CodeModel)
admin.site.register(ItemModel, ItemModelAdmin)
