from dal import autocomplete

from .models import TestModel


class TestForm(autocomplete.FutureModelForm):
    test = autocomplete.TagulousField(
        required=False,
        queryset=TestModel.test.tag_model.objects.all(),
        widget=autocomplete.TagSelect2(url='select2_tagulous'),
    )

    class Meta:
        model = TestModel
        fields = ('name', 'test')
