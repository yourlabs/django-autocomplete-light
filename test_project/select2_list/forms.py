from dal import autocomplete

from django import forms

from .models import TModel


def get_choice_list():
    return [model.test for model in TModel.objects.all()]


def get_choice_list_with_id():
    return [[str(model.id), model.test] for model in TModel.objects.all()]


class TForm(forms.ModelForm):
    test = autocomplete.Select2ListCreateChoiceField(
        choice_list=get_choice_list,
        required=False,
        widget=autocomplete.ListSelect2(url='select2_list')
    )
