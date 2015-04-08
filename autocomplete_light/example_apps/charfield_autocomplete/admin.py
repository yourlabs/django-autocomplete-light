from django.contrib import admin
from forms import TaggableForm
from models import Taggable


class TaggableInline(admin.TabularInline):
    form = TaggableForm
    model = Taggable


class TaggableAdmin(admin.ModelAdmin):
    form = TaggableForm
    list_display = ['name', 'tags']
    inlines = [TaggableInline]

admin.site.register(Taggable, TaggableAdmin)
