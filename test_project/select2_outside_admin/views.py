try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views import generic

from select2_many_to_many.forms import TForm
from select2_many_to_many.models import TModel


class UpdateView(generic.UpdateView):
    model = TModel
    form_class = TForm
    template_name = 'select2_outside_admin.html'
    success_url = reverse_lazy('select2_outside_admin')

    def get_object(self):
        return TModel.objects.first()
