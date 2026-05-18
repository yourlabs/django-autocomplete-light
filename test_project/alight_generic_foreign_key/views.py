from django.views import generic

from .forms import TForm
from .models import TModel


class TestView(generic.UpdateView):
    model = TModel
    form_class = TForm
    template_name = 'form.html'

    def get_success_url(self):
        return self.request.path
