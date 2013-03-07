from django.contrib import admin
from hvad.admin import TranslatableAdmin
import autocomplete_light

from .models import Category, Item

class CategoryAdmin(TranslatableAdmin):
#    form = autocomplete_light.modelform_factory(Category)
    list_display = ('lazy_name', 'lazy_language',
                    'get_available_languages', )
    model = Category

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item)
