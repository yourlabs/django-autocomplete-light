from django import forms

from dal import autocomplete

from .models import TModel


class TForm(forms.ModelForm):
    tags = autocomplete.AlightListCreateChoiceField(
        choice_list=['django', 'python', 'javascript', 'css'],
        widget=autocomplete.TagAlight(url='alight_tag'),
        required=False,
    )

    class Meta:
        model = TModel
        fields = ('tags',)
