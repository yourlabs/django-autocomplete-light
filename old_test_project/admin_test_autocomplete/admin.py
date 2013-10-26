from django.contrib import admin

import autocomplete_light

from models import Foo, Bar


class FooInline(admin.TabularInline):
    model = Foo


class FooAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Foo)
admin.site.register(Foo, FooAdmin)


class BarAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Bar)
    inlines = [FooInline]
admin.site.register(Bar, BarAdmin)
