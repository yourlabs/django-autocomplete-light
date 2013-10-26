from django import forms

import autocomplete_light

from models import Relationship


class RelationshipForm(autocomplete_light.GenericModelForm):
    person = autocomplete_light.GenericModelChoiceField(
        widget=autocomplete_light.ChoiceWidget(
            autocomplete='AutocompletePeople',
            autocomplete_js_attributes={'minimum_characters': 0}))

    class Meta:
        model = Relationship
        exclude = ('person_content_type', 'person_object_id')
