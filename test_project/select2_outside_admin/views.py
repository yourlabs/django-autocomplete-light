from django.core.urlresolvers import reverse_lazy
from django.views import generic

from select2_many_to_many.forms import TestForm
from select2_many_to_many.models import TestModel


class UpdateView(generic.UpdateView):
    model = TestModel
    form_class = TestForm
    template_name = 'select2_outside_admin.html'
    success_url = reverse_lazy('select2_outside_admin')

    def get_object(self):
        return TestModel.objects.first()
