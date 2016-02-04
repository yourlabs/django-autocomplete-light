from dal import autocomplete

from .models import TestModel


class TestForm(autocomplete.FutureModelForm):
    test = autocomplete.CreateModelField(
        required=False,
        queryset=TestModel.objects.all(),
        widget=autocomplete.ModelSelect2(
            'select2_one_to_one_autocomplete')
    )

    class Meta:
        model = TestModel
        fields = ('name', 'test')
