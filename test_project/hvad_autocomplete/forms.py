from django import forms

import autocomplete_light

from .models import Category, Item

class ItemForm(forms.ModelForm):
    class Meta:
        widgets = autocomplete_light.get_widgets_dict(Item)
        model = Item
        fields = ('category', )
