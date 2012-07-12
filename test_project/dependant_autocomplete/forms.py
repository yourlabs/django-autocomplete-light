from django import forms

import autocomplete_light

from models import Dummy


class DummyForm(forms.ModelForm):
    class Media:
        js = ('dependant_autocomplete.js',)

    class Meta:
        model = Dummy
        widgets = autocomplete_light.get_widgets_dict(Dummy)
        #widgets.update({
            #'city': autocomplete_light.ChoiceWidget('CityAutocomplete',
                #widget_js_attributes={'bootstrap': 'dependant_autocomplete'})})
