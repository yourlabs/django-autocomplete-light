from __future__ import unicode_literals

import unittest
import pytest

from django import VERSION
from django.utils.encoding import force_text

from autocomplete_light.example_apps.autocomplete_test_case_app.models import (
        NonIntegerPk, SubGroup, CustomSchema, CustomIntegerPk, Caps)
from .case import *


class AutocompleteModelMock(autocomplete_light.AutocompleteModelBase):
    limit_choices = 2
    choices = User.objects.all()
    search_fields = ('username', 'email')


class FormMock(forms.Form):
    x = forms.ModelChoiceField(queryset=AutocompleteModelMock.choices,
        widget=autocomplete_light.ChoiceWidget(
            autocomplete=AutocompleteModelMock))


class MultipleFormMock(forms.Form):
    x = forms.ModelMultipleChoiceField(queryset=AutocompleteModelMock.choices,
        widget=autocomplete_light.MultipleChoiceWidget(
            autocomplete=AutocompleteModelMock))


class AutocompleteModelTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteModelMock

    def assert_choices_equal(self, result, test):
        self.assertEqual([x.pk for x in result],
                         [x.pk for x in test['expected']])

    def get_choices_for_values_tests(self):
        return (
            {
                'fixture': [1, 4],
                'expected': [
                    self.abe,
                    self.john,
                ]
            },
            {
                'fixture': [4, 1],
                'expected': [
                    self.john,
                    self.abe,
                ]
            },
        )

    def get_choices_for_request_tests(self):
        return (
            {
                'fixture': make_get_request('q=j'),
                'kwargs': {
                    'limit_choices': 5,
                },
                'expected': [
                    self.jack,
                    self.james,
                    self.john,
                ]
            },
            {
                'fixture': make_get_request('q=j'),
                'kwargs': {
                    'order_by': '-username',
                    'limit_choices': 5,
                },
                'expected': [
                    self.john,
                    self.james,
                    self.jack,
                ]
            },
            {
                'fixture': make_get_request('q=j'),
                'kwargs': {
                    'order_by': ('-email', 'username'),
                    'limit_choices': 5,
                },
                'expected': [
                    self.james,
                    self.john,
                    self.jack,
                ]
            },
            {
                'fixture': make_get_request('q=sale'),
                'expected': [
                    self.abe,
                    self.james,
                ]
            },
            {
                'fixture': make_get_request(),
                'expected': [
                    self.abe,
                    self.jack,
                ]
            },
        )

    def get_validate_tests(self):
        return (
            {
                'fixture': [1, 4],
                'expected': True,
            },
            {
                'fixture': [1, 4, 123],
                'expected': False,
            },
        )

    def get_autocomplete_html_tests(self):
        return (
            {
                'fixture': make_get_request('q=j'),
                'expected': ''.join([
                    '<span data-value="%s">%s</span>' % (
                        self.jack.pk, force_text(self.jack)),
                    '<span data-value="%s">%s</span>' % (
                        self.james.pk, force_text(self.james)),
                ])
            },
            {
                'fixture': make_get_request(),
                'expected': ''.join([
                    '<span data-value="%s">%s</span>' % (
                        self.abe.pk, force_text(self.abe)),
                    '<span data-value="%s">%s</span>' % (
                        self.jack.pk, force_text(self.jack)),
                ])
            },
        )

    def get_widget_tests(self):
        return (
            {
                'form_class': FormMock,
                'fixture': 'x=4',
                'expected_valid': True,
                'expected_data': self.john,
            },
            {
                'form_class': FormMock,
                'fixture': 'x=3&x=4',
                'expected_valid': True,
                'expected_data': self.john,
            },
            {
                'fixture': 'x=abc',
                'expected_valid': False,
            },
            {
                'form_class': MultipleFormMock,
                'fixture': 'x=4&x=2',
                'expected_valid': True,
                'expected_data': [self.jack, self.john],
            },
            {
                'fixture': 'x=abc&x=2',
                'expected_valid': False,
            },
        )

    @unittest.skipIf(VERSION < (1, 8), 'Django < 1.8')
    def test_queryset_mistake(self):
        class Test(autocomplete_light.AutocompleteModelBase):
            choices = NonIntegerPk.objects.select_related('artist')

        fixture = Test(values=[NonIntegerPk.objects.create(name='bal').pk])
        results = fixture.choices_for_values()

        with pytest.raises(Exception):
            len(results)

    def test_ambiguous_column_name(self):
        class Test(autocomplete_light.AutocompleteModelBase):
            choices = NonIntegerPk.objects.select_related('noise')

        fixture = Test(values=[NonIntegerPk.objects.create(name='bal').pk])
        # Call len to force evaluate queryset
        len(fixture.choices_for_values())

    def test_inherited_model_ambiguous_column_name(self):
        subgroup = SubGroup.objects.create(name='test')

        class Test(autocomplete_light.AutocompleteModelBase):
            choices = SubGroup.objects.all()

        fixture = Test(values=[subgroup.pk])
        assert fixture.choices_for_values()[0] == subgroup

    def test_custom_table_and_name(self):
        obj = CustomSchema.objects.create(name='test')

        class Test(autocomplete_light.AutocompleteModelBase):
            choices = CustomSchema.objects.all()

        fixture = Test(values=[obj.pk])
        assert fixture.choices_for_values()[0] == obj

    def test_primary_key_zero(self):
        obj = CustomIntegerPk.objects.create(id=0)

        class Test(autocomplete_light.AutocompleteModelBase):
            choices = CustomIntegerPk.objects.all()

        fixture = Test(values=[obj.pk])
        self.assertEqual(list(fixture.choices_for_values()), [obj])

    def test_list_ordering(self):
        class Fixture(AutocompleteModelMock):
            order_by = ['id']

        fixture = Fixture(values=[1, 4])
        self.assertEqual(list(fixture.choices_for_values()), [self.abe, self.john])

    def test_caps(self):
        obj = Caps.objects.create(id=7, name='test')

        class Test(autocomplete_light.AutocompleteModelBase):
            choices = Caps.objects.all()

        fixture = Test(values=[obj.pk])
        assert fixture.choices_for_values()[0] == obj
