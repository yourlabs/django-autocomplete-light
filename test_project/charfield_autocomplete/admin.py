from django.contrib import admin
from django import forms

import autocomplete_light

from models import Address

class AddressForm(forms.ModelForm):
    city =  forms.CharField(
        max_length=100,
        widget=autocomplete_light.widgets.ChoiceWidget('CityListAutocomplete'))

    class Meta:
        model = Address

class AddressAdmin(admin.ModelAdmin):
    form = AddressForm

admin.site.register(Address, AddressAdmin)
