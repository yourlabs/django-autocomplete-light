from django.contrib import admin
from django import forms

import autocomplete_light

from models import Address, CityOrSomethingElse

class AddressFormStrict(forms.ModelForm):
    city =  forms.CharField(
        max_length=100,
        widget=autocomplete_light.widgets.ChoiceWidget(
            'CityListAutocompleteStrict'))

    class Meta:
        model = Address

class AddressAdmin(admin.ModelAdmin):
    form = AddressFormStrict

admin.site.register(Address, AddressAdmin)


class CityOrSomethingElseForm(forms.ModelForm):
    city_or_something_else =  forms.CharField(
        max_length=100,
        widget=autocomplete_light.widgets.ChoiceWidget(
            'CityListAutocompleteLoose'))

    class Meta:
        model = CityOrSomethingElse

class CityOrSomethingElseAdmin(admin.ModelAdmin):
    form = CityOrSomethingElseForm

admin.site.register(CityOrSomethingElse, CityOrSomethingElseAdmin)
