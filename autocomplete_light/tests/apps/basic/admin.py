from django.contrib import admin

try:
    import genericm2m
except ImportError:
    genericm2m = None

try:
    import taggit
except ImportError:
    taggit = None

from .models import *
from .forms import *


class FkInline(admin.TabularInline):
    model = FkModel
    form = FkModelForm


class FkModelAdmin(admin.ModelAdmin):
    form = FkModelForm
    inlines = [FkInline]
admin.site.register(FkModel, FkModelAdmin)


class OtoModelAdmin(admin.ModelAdmin):
    form = OtoModelForm
admin.site.register(OtoModel, OtoModelAdmin)


class MtmModelAdmin(admin.ModelAdmin):
    form = MtmModelForm
admin.site.register(MtmModel, MtmModelAdmin)


class GfkModelAdmin(admin.ModelAdmin):
    form = GfkModelForm
admin.site.register(GfkModel, GfkModelAdmin)


if genericm2m:
    class GmtmModelAdmin(admin.ModelAdmin):
        form = GmtmModelForm
    admin.site.register(GmtmModel, GmtmModelAdmin)


if taggit:
    class TaggitModelAdmin(admin.ModelAdmin):
        form = TaggitModelForm
    admin.site.register(TaggitModel, TaggitModelAdmin)
