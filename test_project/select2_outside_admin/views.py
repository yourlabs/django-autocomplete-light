try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.forms import inlineformset_factory
from django.views import generic

from select2_many_to_many.forms import TForm
from select2_many_to_many.models import TModel


class UpdateView(generic.UpdateView):
    model = TModel
    form_class = TForm
    template_name = 'select2_outside_admin.html'
    success_url = reverse_lazy('select2_outside_admin')
    formset_class = inlineformset_factory(
        TModel,
        TModel,
        form=TForm,
        extra=1,
        fk_name='for_inline',
        fields=('name', 'test')
    )

    def get_object(self):
        return TModel.objects.first()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid() and self.formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        result = super().form_valid(form)
        self.formset.save()
        return result

    @property
    def formset(self):
        if '_formset' not in self.__dict__:
            setattr(self, '_formset', self.formset_class(
                self.request.POST if self.request.method == 'POST' else None,
                instance=getattr(self, 'object', self.get_object()),
            ))
        return self._formset
