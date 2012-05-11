from django.contrib import admin

import autocomplete_light

from models import Address, Contact
from forms import AddressForm

class AddressInline(admin.TabularInline):
    model = Address
    form = AddressForm

class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
admin.site.register(Address, AddressAdmin)

class ContactAdmin(admin.ModelAdmin):
    inlines = (AddressInline,)
admin.site.register(Contact, ContactAdmin)
