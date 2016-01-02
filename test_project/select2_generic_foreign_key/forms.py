from dal import autocomplete

from django.contrib.auth.models import Group

from .models import TestModel


class TestForm(autocomplete.FutureModelForm):
    test = autocomplete.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Group.objects.all(),
            TestModel.objects.all(),
        ),
        required=False,
        widget=autocomplete.QuerySetSequenceSelect2('select2_gfk'),
    )

    class Meta:
        model = TestModel
        fields = ('name',)
