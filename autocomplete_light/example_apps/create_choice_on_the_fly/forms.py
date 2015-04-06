import autocomplete_light.shortcuts as autocomplete_light

from .models import Fly


class FlyForm(autocomplete_light.ModelForm):
    class Meta:
        model = Fly
        fields = ('name', 'other_fly')
        widgets = {
            'other_fly': autocomplete_light.ChoiceWidget(
                'FlyAutocomplete', widget_attrs={'data-widget-bootstrap':
                    'fly-widget'})
        }
