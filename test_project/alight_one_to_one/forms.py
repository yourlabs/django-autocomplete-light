from dal import autocomplete

from .models import TModel


class TForm(autocomplete.FutureModelForm):
    class Meta:
        model = TModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.ModelAlight(
                'alight_one_to_one_autocomplete'
            )
        }
