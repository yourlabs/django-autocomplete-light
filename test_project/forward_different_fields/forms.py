from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

from dal import autocomplete, forward

from django import forms

from .models import TModel


class TForm(forms.ModelForm):
    CHOICES = (("a", "Alice"), ("b", "Bob"), ("c", "Charlie"))
    POOR_CHOICE = (("d", "Dylan"), )

    checkbox = forms.BooleanField(required=False)
    select = forms.ChoiceField(required=False,
                               choices=CHOICES)
    select_radio = forms.ChoiceField(required=False,
                                     widget=RadioSelect(),
                                     choices=CHOICES)
    multiselect = forms.MultipleChoiceField(required=False,
                                            choices=CHOICES)
    multiselect_checks = forms.MultipleChoiceField(
        required=False,
        widget=CheckboxSelectMultiple(),
        choices=CHOICES)

    multiselect_checks_poor = forms.MultipleChoiceField(
        required=False,
        widget=CheckboxSelectMultiple(),
        choices=POOR_CHOICE)

    test = autocomplete.Select2ListChoiceField(
        required=False,
        widget=autocomplete.ListSelect2(
            url='forward_different_fields',
            forward=("name",
                     "checkbox",
                     "select",
                     "select_radio",
                     "multiselect",
                     "multiselect_checks",
                     forward.Field(src="multiselect_checks_poor",
                                   strategy=forward.FieldStrategy.MULTIPLE))

        )
    )

    class Meta:
        model = TModel
        fields = ('name',
                  'checkbox',
                  'select',
                  'select_radio',
                  'multiselect',
                  'multiselect_checks',
                  'multiselect_checks_poor',
                  'test')

