from django.contrib import admin

import autocomplete_light

from models import Address, Contact, TaggedItem
from forms import AddressForm, TaggedItemForm

class AddressInline(admin.TabularInline):
    model = Address
    form = AddressForm

class TaggedItemInline(admin.TabularInline):
    model = TaggedItem
    form = TaggedItemForm

class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
admin.site.register(Address, AddressAdmin)

class ContactAdmin(admin.ModelAdmin):
    inlines = (AddressInline, TaggedItemInline)
admin.site.register(Contact, ContactAdmin)

class TaggedItemAdmin(admin.ModelAdmin):
    form = TaggedItemForm
admin.site.register(TaggedItem, TaggedItemAdmin)
