from django import forms

from .models import TModel
from .widgets import TModelSelect2


class TForm(forms.ModelForm):
    class Meta:
        model = TModel
        fields = ('name', 'test')
        widgets = {
            'test': TModelSelect2(url='select2_fk')
        }
