from __future__ import unicode_literals

from cities_light.models import City
from django.contrib.contenttypes.models import ContentType

from ...example_apps.autocomplete_test_case_app.models import Group, User
from .case import *


class AutocompleteGenericMock(autocomplete_light.AutocompleteGenericBase):
    choices = (
        User.objects.filter(pk__lt=10),
        Group.objects.filter(pk__lt=10),
    )
    search_fields = (
        ('username', 'email'),
        ('name',),
    )
    limit_choices = 3


class FormMock(forms.Form):
    x = autocomplete_light.GenericModelChoiceField(
        widget=autocomplete_light.ChoiceWidget(
            autocomplete=AutocompleteGenericMock))


class AutocompleteGenericTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteGenericMock

    def assert_choices_equal(self, result, test):
        self.assertEqual(list(result), test['expected'])

    def get_choices_for_values_tests(self):
        return (
            {
                'fixture': [
                    '%s-%s' % (self.user_ctype.pk, self.james.pk),
                    '%s-%s' % (self.group_ctype.pk, self.bluesmen.pk),
                ],
                'expected': [
                    self.james,
                    self.bluesmen,
                ]
            },
            {
                'fixture': [
                    '%s-%s' % (self.user_ctype.pk, self.james.pk),
                    '%s-%s' % (self.user_ctype.pk, self.elton.pk),
                    '%s-%s' % (self.group_ctype.pk, self.bluesmen.pk),
                    '%s-%s' % (self.group_ctype.pk, self.emos.pk),
                ],
                'expected': [
                    self.james,
                    self.bluesmen,
                ],
                'name': 'should ignore values that are not in the querysets',
            },
        )

    def get_choices_for_request_tests(self):
        return (
            {
                'fixture': make_get_request('j'),
                'expected': [
                    self.abe,
                    self.rockers,
                    self.bluesmen,
                ],
            },
            {
                'fixture': make_get_request('q=elton'),
                'expected': [],
                'name': 'should not propose models that are not in the qs',
            },
        )

    def get_validate_tests(self):
        return (
            {
                'fixture': [
                    '%s-%s' % (self.user_ctype.pk, self.james.pk),
                    '%s-%s' % (self.group_ctype.pk, self.bluesmen.pk),
                    '%s-%s' % (self.group_ctype.pk, self.emos.pk),
                ],
                'expected': False,
            },
            {
                'fixture': [
                    '%s-%s' % (self.user_ctype.pk, self.james.pk),
                    '%s-%s' % (self.group_ctype.pk, self.bluesmen.pk),
                ],
                'expected': True,
            },
            {
                'fixture': [],
                'expected': True,
            },
            {
                'fixture': ['bla'],
                'expected': False,
            },
            {
                'fixture': ['123123-123123'],
                'expected': False,
            },
        )

    def get_autocomplete_html_tests(self):
        return []

    def get_widget_tests(self):
        return (
            {
                'form_class': FormMock,
                'fixture': 'x=%s-%s' % (
                    self.group_ctype.pk, self.bluesmen.pk),
                'expected_valid': True,
                'expected_data': self.bluesmen,
            },
            {
                'form_class': FormMock,
                'fixture': 'x=%s-%s' % (
                    self.group_ctype.pk, self.emos.pk),
                'expected_valid': False,
            },
            {
                'form_class': FormMock,
                'fixture': 'x=12343-2',
                'expected_valid': False,
            },
            {
                'form_class': FormMock,
                'fixture': 'x=%s-2' % ContentType.objects.get_for_model(
                    City).pk,
                'expected_valid': False,
            },
        )

    def test_default_search_fields(self):
        class MyGeneric(autocomplete_light.AutocompleteGenericBase):
            choices = [Group.objects.all()]
        self.assertEqual(MyGeneric.search_fields, [('name',)])
