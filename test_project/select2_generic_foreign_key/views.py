from django.views import generic

from .forms import TestForm
from .models import TestModel


class TestView(generic.UpdateView):
    model = TestModel
    form_class = TestForm
    template_name = 'form.html'

    def get_success_url(self):
        return self.request.path
