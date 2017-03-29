from django.forms import ModelForm
from dal import autocomplete
from .models import ModelOne, ModelTwo, MasterModel


class Form1(ModelForm):
    class Meta:
        model = MasterModel
        fields = ('name', 'modelone')
        widgets = {
            'modelone': autocomplete.ModelSelect2Multiple(
                url='modelone-autocomplete')
        }


class Form2(ModelForm):
    class Meta:
        model = MasterModel
        fields = ('modeltwo', )
        widgets = {
            'modeltwo': autocomplete.ModelSelect2Multiple(
                url='modeltwo-autocomplete'),
        }
