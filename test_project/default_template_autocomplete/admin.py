from django.contrib import admin

import autocomplete_light

from models import TemplatedChoice, TestModel

class TestModelAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(TestModel)

admin.site.register(TestModel, TestModelAdmin)
admin.site.register(TemplatedChoice)