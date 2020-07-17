from dal import autocomplete
from dal.forms import FutureModelForm

from django import forms

from .models import TModel


class TForm(FutureModelForm):
    test = autocomplete.ModelAlight(queryset=TModel.objects.all())

    class Meta:
        model = TModel
        fields = ('name', 'test')
