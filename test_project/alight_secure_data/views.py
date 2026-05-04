from dal import autocomplete

from .models import TModel


class SecureDataView(autocomplete.AlightQuerySetView):
    def get_queryset(self):
        return TModel.objects.filter(owner=self.request.user)
