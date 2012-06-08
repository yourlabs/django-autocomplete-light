from django.contrib import admin

import autocomplete_light

from models import Address, Contact, TaggedItem
from generic_form_example import TaggedItemForm

class AddressInline(admin.TabularInline):
    model = Address
    form = autocomplete_light.modelform_factory(Address)

class TaggedItemInline(admin.TabularInline):
    model = TaggedItem
    form = TaggedItemForm

class AddressAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Address)
admin.site.register(Address, AddressAdmin)

class ContactAdmin(admin.ModelAdmin):
    inlines = (AddressInline, TaggedItemInline)
admin.site.register(Contact, ContactAdmin)

class TaggedItemAdmin(admin.ModelAdmin):
    form = TaggedItemForm
admin.site.register(TaggedItem, TaggedItemAdmin)
