from dal import autocomplete

from .models import TModel


class SecureDataView(autocomplete.AlightQuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TModel.objects.none()
        return TModel.objects.filter(owner=self.request.user)
