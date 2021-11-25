from django.contrib import admin

from .models import TModel


class TestInline(admin.TabularInline):
    model = TModel
    fk_name = 'for_inline'


class TestAdmin(admin.ModelAdmin):
    inlines = [TestInline]
admin.site.register(TModel, TestAdmin)
