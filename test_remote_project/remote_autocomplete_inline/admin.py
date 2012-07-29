
from django.contrib import admin

import autocomplete_light

from models import *


class AddressInline(admin.TabularInline):
    model = Address
    form = autocomplete_light.modelform_factory(Address)


class AddressAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Address)
    inlines = [AddressInline]
admin.site.register(Address, AddressAdmin)
