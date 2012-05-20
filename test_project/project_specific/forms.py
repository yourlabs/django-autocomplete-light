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


class TaggedItemForm(autocomplete_light.GenericModelForm):
    content_object = autocomplete_light.GenericForeignKeyField(
        widget=autocomplete_light.AutocompleteWidget(
            'MyGenericChannel', max_items=1))

    class Meta:
        model = TaggedItem
        exclude = (
            'content_type',
            'object_id',
        )
