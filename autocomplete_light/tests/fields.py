from __future__ import unicode_literals

import unittest

from django import forms

import autocomplete_light


class BaseTestCase(unittest.TestCase):
    GOOD_VALUE = 'b'
    BAD_VALUE = 'xx'

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

    def test_select_choice(self):
        class TestForm(forms.Form):
            test_field = self.field_class(self.TestAutocomplete)

        form = TestForm({'test_field': self.GOOD_VALUE})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['test_field'], self.GOOD_VALUE)


class ChoiceFieldTestCase(BaseTestCase):
    field_class = autocomplete_light.ChoiceField


class MultipleChoiceFieldTestCase(BaseTestCase):
    field_class = autocomplete_light.MultipleChoiceField
    GOOD_VALUE = ['b']


class ModelChoiceFieldTestCase(BaseTestCase):
    pass


class ModelMultipleChoiceFieldTestCase(BaseTestCase):
    pass


class GenericModelChoiceFieldTestCase(BaseTestCase):
    pass


class GenericModelMultipleChoiceFieldTestCase(BaseTestCase):
    pass
