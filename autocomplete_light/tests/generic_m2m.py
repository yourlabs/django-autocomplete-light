from autocomplete.case import *
from autocomplete.generic import AutocompleteGenericMock, AutocompleteGenericTestCase

from django import http
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission

from autocomplete_light.contrib.generic_m2m import GenericModelForm, \
    GenericModelMultipleChoiceField

from generic_m2m_autocomplete.models import ModelGroup


class FormMock(GenericModelForm):
    related = GenericModelMultipleChoiceField(
        widget=autocomplete_light.MultipleChoiceWidget(
            AutocompleteGenericMock))

    class Meta:
        model = ModelGroup


class AutocompleteGenericM2MTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteGenericMock

    def setUp(self):
        self.setUpAuth()

    def test_form(self):
        tests = (
            {
                'fixture': 'name=foo&related=%s-%s' % (
                    self.group_ctype.pk, self.bluesmen.pk),
                'valid': True,
                'result': [self.bluesmen],
            },
            {
                'fixture': 'name=foo&related=%s-%s&related=%s-%s' % (
                    self.group_ctype.pk, self.rockers.pk,
                    self.user_ctype.pk, self.james.pk),
                'valid': True,
                'result': [self.james, self.rockers],
            },
        )

        instance = None
        for test in tests:
            form = FormMock(http.QueryDict(test['fixture']),
                instance=instance)

            self.assertEqual(form.is_valid(), test['valid'])
            instance = form.save()

            self.assertEqual(instance.related.all().generic_objects(),
                test['result'])
