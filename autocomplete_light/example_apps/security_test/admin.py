from django.contrib import admin

from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'private')
    list_editable = ('private',)
admin.site.register(Item, ItemAdmin)
