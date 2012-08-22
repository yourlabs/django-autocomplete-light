from django.contrib import admin

from forms import TaggableForm
from models import Taggable


class TaggableAdmin(admin.ModelAdmin):
    form = TaggableForm
    list_display = ['name', 'tags']

admin.site.register(Taggable, TaggableAdmin)
