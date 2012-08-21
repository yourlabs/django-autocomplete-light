from django.contrib import admin

import autocomplete_light

from clickable.models import ClickableItem, ClickableItemContainer

class ClickableItemContainerAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(ClickableItemContainer)

admin.site.register(ClickableItemContainer, ClickableItemContainerAdmin)
admin.site.register(ClickableItem)

