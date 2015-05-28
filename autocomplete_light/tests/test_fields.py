from __future__ import unicode_literals

import pytest

import autocomplete_light.shortcuts as autocomplete_light
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ..example_apps.basic.models import GfkModel
from ..example_apps.security_test.models import Item


class BaseMixin(object):
    GOOD_VALUE = 'b'
    CLEANED_VALUE = 'b'
    BAD_VALUE = 'xx'
    EMPTY_VALUE = None

    class TestAutocomplete(autocomplete_light.AutocompleteListBase):
        choices = ['a', 'b', 'c']

    def test_automatic_field_choices(self):
        test = self.field_class(self.TestAutocomplete)
        self.assertEqual(test.choices, [('a', 'a'), ('b', 'b'), ('c', 'c')])

    def test_validate(self):
        test = self.field_class(self.TestAutocomplete)
        test.validate(self.GOOD_VALUE)

        with self.assertRaises(forms.ValidationError):
            test.validate(self.BAD_VALUE)

    def test_validate_required(self):
        test = self.field_class(self.TestAutocomplete, required=True)

        with pytest.raises(forms.ValidationError):
            test.validate(self.EMPTY_VALUE)

    def test_select_choice(self):
        class TestForm(forms.Form):
            test_field = self.field_class(self.TestAutocomplete)

        form = TestForm({'test_field': self.GOOD_VALUE})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['test_field'], self.CLEANED_VALUE)


class ChoiceFieldTestCase(BaseMixin, TestCase):
    field_class = autocomplete_light.ChoiceField


class MultipleChoiceFieldTestCase(BaseMixin, TestCase):
    field_class = autocomplete_light.MultipleChoiceField
    GOOD_VALUE = ['b']
    CLEANED_VALUE = ['b']


class ModelChoiceFieldTestCase(BaseMixin, TestCase):
    fixtures = ['security_test.json']
    field_class = autocomplete_light.ModelChoiceField
    GOOD_VALUE = 1
    BAD_VALUE = 2

    def setUp(self):
        self.CLEANED_VALUE = Item.objects.get(pk=self.GOOD_VALUE)

    class TestAutocomplete(autocomplete_light.AutocompleteModelBase):
        choices = Item.objects.filter(private=False)

    def test_automatic_field_choices(self):
        test = self.field_class(self.TestAutocomplete, required=True)
        self.assertEqual(list(test.choices),
                         [('', '---------'), (1, 'public'), (3, 'linked')])


class ModelMultipleChoiceFieldTestCase(ModelChoiceFieldTestCase):
    field_class = autocomplete_light.ModelMultipleChoiceField
    GOOD_VALUE = [1]
    BAD_VALUE = [2]

    def setUp(self):
        self.CLEANED_VALUE = Item.objects.filter(pk=1)

    def test_automatic_field_choices(self):
        test = self.field_class(self.TestAutocomplete, required=True)
        self.assertEqual(list(test.choices),
                         [(1, 'public'), (3, 'linked')])

    def test_select_choice(self):
        class TestForm(forms.Form):
            test_field = self.field_class(self.TestAutocomplete)

        form = TestForm({'test_field': self.GOOD_VALUE})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.cleaned_data['test_field']),
                         len(self.CLEANED_VALUE))
        self.assertEqual(form.cleaned_data['test_field'][0],
                         self.CLEANED_VALUE[0])


class CustomModelChoiceField(forms.ModelChoiceField):
    pass


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    pass


class CustomAutocompleteModelChoiceField(autocomplete_light.FieldBase,
                                         CustomModelChoiceField):
    """ Autocomplete form field which inherently, but not directly, inherits
    forms.ModelChoiceField
    """
    widget = autocomplete_light.ChoiceWidget


class CustomAutocompleteModelMultipleChoiceField(autocomplete_light.FieldBase,
                                                 CustomModelMultipleChoiceField):
    """ Autocomplete form field which inherently, but not directly, inherits
    forms.ModelMultipleChoiceField
    """
    widget = autocomplete_light.MultipleChoiceWidget


class CustomModelFieldTestCase(ModelChoiceFieldTestCase):
    """ Regression test for a custom ModelChoiceField
    https://github.com/yourlabs/django-autocomplete-light/issues/379
    """
    field_class = CustomAutocompleteModelChoiceField


class CustomMultipleModelFieldTestCase(ModelMultipleChoiceFieldTestCase):
    """ Regression test for a custom ModelMultipleChoiceField
    https://github.com/yourlabs/django-autocomplete-light/issues/379
    """
    field_class = CustomAutocompleteModelMultipleChoiceField


class GenericModelChoiceFieldTestCase(BaseMixin, TestCase):
    field_class = autocomplete_light.GenericModelChoiceField
    fixtures = ['basic_gfk_gmtm.json']

    class TestAutocomplete(autocomplete_light.AutocompleteGenericBase):
        choices = [GfkModel.objects.all()]

    def setUp(self):
        self.gfk_ct = ContentType.objects.get_for_model(GfkModel)
        self.GOOD_VALUE = '%s-%s' % (self.gfk_ct.pk, 1)
        self.BAD_VALUE = '%s-%s' % (self.gfk_ct.pk, 1234)
        self.CLEANED_VALUE = GfkModel.objects.get(pk=1)

    def test_automatic_field_choices(self):
        pass  # generic model choice field has no choices



class GenericModelMultipleChoiceFieldTestCase(GenericModelChoiceFieldTestCase):
    field_class = autocomplete_light.GenericModelMultipleChoiceField

    def setUp(self):
        self.gfk_ct = ContentType.objects.get_for_model(GfkModel)
        self.GOOD_VALUE = ['%s-%s' % (self.gfk_ct.pk, 1)]
        self.BAD_VALUE = ['%s-%s' % (self.gfk_ct.pk, 1234)]
        self.CLEANED_VALUE = [GfkModel.objects.get(pk=1)]

    def test_automatic_field_choices(self):
        pass  # generic model choice field has no choices
