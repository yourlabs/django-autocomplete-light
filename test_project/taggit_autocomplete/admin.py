from django.contrib import admin
from models import TaggitDemo
from forms import TaggitDemoForm

class TaggitDemoAdmin(admin.ModelAdmin):
    model = TaggitDemo
    form = TaggitDemoForm

admin.site.register(TaggitDemo, TaggitDemoAdmin)
