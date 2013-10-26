from django import forms

import autocomplete_light
from cities_light.models import City

from models import Event


class ScheduleForm(forms.ModelForm):
    street = forms.CharField(label='Street', max_length=30, required=False)
    city = forms.ModelChoiceField(label='City', queryset=City.objects.all(),
                widget=autocomplete_light.ChoiceWidget('CityAutocomplete'))

    class Meta:
        model = Event
