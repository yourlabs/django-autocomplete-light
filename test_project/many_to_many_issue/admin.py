from django.contrib import admin
from many.models import Cat, TestMany
from autocomplete_light import shortcuts as al


class CatAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cat, CatAdmin)


class TestManyAdmin(admin.ModelAdmin):
    form = al.modelform_factory(TestMany, fields='__all__')


admin.site.register(TestMany, TestManyAdmin)
