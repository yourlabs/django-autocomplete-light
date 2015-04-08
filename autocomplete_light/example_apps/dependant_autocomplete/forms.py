import autocomplete_light
from django import forms

from .models import Dummy


class DummyForm(autocomplete_light.ModelForm):
    class Media:
        """
        We're currently using Media here, but that forced to move the
        javascript from the footer to the extrahead block ...

        So that example might change when this situation annoys someone a lot.
        """
        js = ('dependant_autocomplete.js',)

    class Meta:
        model = Dummy
        exclude = []
