from django import forms

import autocomplete_light
from cities_light.models import City
from cities_light.contrib.autocomplete_light_widgets import CityAutocompleteWidget

from models import Address, TaggedItem

class AddressForm(forms.ModelForm):
    city = forms.ModelChoiceField(City.objects.all(),
        widget=CityAutocompleteWidget('CityChannel', max_items=1))
        
    class Meta:
        model = Address
        widgets = autocomplete_light.get_widgets_dict(Address, 
            autocomplete_exclude='city')


from django.forms import widgets

class TaggedItemForm(forms.ModelForm):
    content_object = forms.CharField()

    class Meta:
        model = TaggedItem
        widgets = {
            'content_type': widgets.Select(),
            'object_id': autocomplete_light.AutocompleteWidget('GenericChannel', bootstrap='generic')
        }
