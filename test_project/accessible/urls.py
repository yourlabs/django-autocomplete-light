from django import forms
from django.views import generic
from django.urls import path, reverse_lazy

from dal import autocomplete

from .models import TModel


class TForm(forms.ModelForm):
    class Meta:
        model = TModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.ModelAccessible(url='select2_fk')
        }


class UpdateView(generic.UpdateView):
    model = TModel
    form_class = TForm
    template_name = 'accessible.html'
    success_url = reverse_lazy('select2_outside_admin')

    def get_object(self):
        return TModel.objects.first()


urlpatterns = [path('', UpdateView.as_view())]
