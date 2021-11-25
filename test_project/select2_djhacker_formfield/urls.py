from dal import autocomplete

from django.conf.urls import url

from .models import TModel


urlpatterns = [
    url(
        'test-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(model=TModel),
        name='select2_djhacker_formfield',
    ),
]


import djhacker
from django import forms
djhacker.formfield(
    TModel.test,
    forms.ModelChoiceField,
    widget=autocomplete.ModelSelect2(url='select2_djhacker_formfield')
)
