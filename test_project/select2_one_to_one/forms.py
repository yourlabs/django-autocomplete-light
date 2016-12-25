from dal import autocomplete

from .models import TModel


class TForm(autocomplete.FutureModelForm):
    class Meta:
        model = TModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.ModelSelect2(
                'select2_one_to_one_autocomplete'
            )
        }
