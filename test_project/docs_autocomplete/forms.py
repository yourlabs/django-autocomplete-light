from django import forms
from django.contrib.auth.models import User
from cities_light.models import City
import autocomplete_light

from models import Profile


class ProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(User.objects.all(),
        widget=autocomplete_light.ChoiceWidget('UserAutocomplete'))

    cities = forms.ModelMultipleChoiceField(City.objects.all(),
        widget=autocomplete_light.MultipleChoiceWidget('CityAutocomplete'))

    class Meta:
        model = Profile
