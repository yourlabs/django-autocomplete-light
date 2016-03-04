from dal import autocomplete

from .models import TestModel


class TestForm(autocomplete.FutureModelForm):
    class Meta:
        model = TestModel
        fields = ('name', 'test')
        widgets = {
            'test': autocomplete.ModelSelect2(
                'select2_one_to_one_autocomplete'
            )
        }
