from django.views import generic
from django.forms.models import modelformset_factory

import autocomplete_light

from models import OutsideAdmin


OutsideAdminModelForm = autocomplete_light.modelform_factory(OutsideAdmin, widgets={
    'tags': autocomplete_light.TextWidget('TagAutocomplete'),})
OutsideAdminModelFormset = modelformset_factory(OutsideAdmin, form=OutsideAdminModelForm)


class FormsetView(generic.FormView):
    form_class = OutsideAdminModelFormset
    template_name = 'inlines_outside_admin/formset.html'
    success_url = '/inlines_outside_admin/'

    def form_valid(self, form):
        form.save()
        return super(FormsetView, self).form_valid(form)
