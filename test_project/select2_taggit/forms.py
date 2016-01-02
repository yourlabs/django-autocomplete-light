from dal import autocomplete

from .models import TestModel


class TestForm(autocomplete.FutureModelForm):
    test = autocomplete.TaggitField(
        required=False,
        widget=autocomplete.TagSelect2(url='select2_taggit'),
    )

    class Meta:
        model = TestModel
        fields = ('name', 'test')
