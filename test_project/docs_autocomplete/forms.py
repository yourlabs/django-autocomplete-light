from django import forms
from django.contrib.auth.models import User
from cities_light.models import City
import autocomplete_light

from models import Profile


class ProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(User.objects.all(),
        widget=autocomplete_light.ChoiceWidget('UserAutocomplete'))

    cities = forms.ModelMultipleChoiceField(City.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget('CityAutocomplete',
            # optionnal: override an autocomplete.js option
            autocomplete_js_attributes={'minimum_characters': 0,
                                        'placeholder': 'Choose 3 cities ...'},
            # optionnal: override a widget.js option
            widget_js_attributes={'max_values': 3}))

    # Note that defining *_js_attributes on Autocomplete classes or instances
    # also work.

    class Meta:
        model = Profile
