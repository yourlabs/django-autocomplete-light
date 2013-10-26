from django.contrib import admin

import autocomplete_light

from models import Address

class AddressAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Address)

admin.site.register(Address, AddressAdmin)
