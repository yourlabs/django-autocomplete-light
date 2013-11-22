from django import forms

import autocomplete_light

from models import Dummy


class DummyForm(forms.ModelForm):
    class Media:
        """
        We're currently using Media here, but that forced to move the
        javascript from the footer to the extrahead block ...

        So that example might change when this situation annoys someone a lot.
        """
        js = ('dependant_autocomplete.js',)

    class Meta:
        model = Dummy
        widgets = autocomplete_light.get_widgets_dict(Dummy)
