from dal import autocomplete

from django.contrib.auth.models import Group

from .models import TestModel


class TestForm(autocomplete.FutureModelForm):
    test = autocomplete.GM2MQuerySetSequenceField(
        queryset=autocomplete.QuerySetSequence(
            Group.objects.all(),
            TestModel.objects.all(),
        ),
        required=False,
        widget=autocomplete.QuerySetSequenceSelect2Multiple(
            'select2_gm2m'),
    )

    class Meta:
        model = TestModel
        fields = ('name',)
