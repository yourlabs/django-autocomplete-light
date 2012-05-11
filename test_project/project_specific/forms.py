from django import forms

import autocomplete_light
from cities_light.models import City
from cities_light.widgets import CityAutocompleteWidget

from models import Address

class AddressForm(forms.ModelForm):
    city = forms.ModelChoiceField(City.objects.all(),
        widget=CityAutocompleteWidget('CityChannel', max_items=1))
        
    class Meta:
        model = Address
