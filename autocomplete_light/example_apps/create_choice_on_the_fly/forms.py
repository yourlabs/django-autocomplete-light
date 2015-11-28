import autocomplete_light.shortcuts as autocomplete_light

from .models import OnTheFly


class OnTheFlyForm(autocomplete_light.ModelForm):
    class Meta:
        model = OnTheFly
        fields = ('name', 'other_fly')
        widgets = {
            'other_fly': autocomplete_light.ChoiceWidget(
                'OnTheFlyAutocomplete', widget_attrs={
                    'data-widget-bootstrap': 'onthefly-widget'})
        }
