from django.urls import re_path as url

from dal import autocomplete

from .models import TModel

urlpatterns = [
    url(
        r'^test-autocomplete/$',
        autocomplete.AlightQuerySetView.as_view(model=TModel),
        name='alight_djhacker_formfield',
    ),
]

import djhacker  # noqa: E402
from django import forms  # noqa: E402

djhacker.formfield(
    TModel.test,
    forms.ModelChoiceField,
    widget=autocomplete.ModelAlight(url='alight_djhacker_formfield'),
)
