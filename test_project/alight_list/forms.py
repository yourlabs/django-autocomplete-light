from django import forms

from dal import autocomplete

from .models import TModel


def get_choice_list():
    return list(
        TModel.objects.exclude(test__isnull=True)
        .exclude(test='')
        .values_list('test', flat=True)
        .distinct()
    )


class TForm(forms.ModelForm):
    test = autocomplete.AlightListCreateChoiceField(
        choice_list=get_choice_list,
        widget=autocomplete.ListAlight(url='alight_list'),
        required=False,
    )

    class Meta:
        model = TModel
        fields = ('name', 'test', 'for_inline')
