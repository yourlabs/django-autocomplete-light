from django.contrib import admin
from hvad.admin import TranslatableAdmin
import autocomplete_light

from .models import Category, Item

class CategoryAdmin(TranslatableAdmin):
    list_display = ('lazy_name', 'lazy_language',
                    'get_available_languages', )
    model = Category

admin.site.register(Category, CategoryAdmin)


class ItemAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Item)
admin.site.register(Item, ItemAdmin)
