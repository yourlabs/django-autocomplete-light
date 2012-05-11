from django.contrib import admin

import autocomplete_light

from forms import AddressForm
from models import Address

class AddressAdmin(admin.ModelAdmin):
    form = AddressForm

admin.site.register(Address, AddressAdmin)
