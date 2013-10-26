from django.contrib import admin

from forms import TaggedItemForm
from models import TaggedItem


class TaggedItemAdmin(admin.ModelAdmin):
    form = TaggedItemForm
admin.site.register(TaggedItem, TaggedItemAdmin)
