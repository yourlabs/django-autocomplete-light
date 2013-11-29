from django import forms

import autocomplete_light

from .models import Item


class DjangoItemForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.filter(private=False))

    class Meta:
        model = Item
        exclude = ('private',)


class AutocompleteItemForm(autocomplete_light.ModelForm):
    class Meta:
        model = Item
        exclude = ('private',)
