from dal import autocomplete

from django import test
from django.core.exceptions import ValidationError


class Select2ListChoiceFieldTest(test.TestCase):

    choice_list = ['windows', 'linux', 'osx']
    choice_list_lists = [
        ['windows_value', 'windows'],
        ['linux_value', 'linux'],
        ['osx_value', 'osx']
    ]
    choice_list_tuples = [
        ('windows_value', 'windows'),
        ('linux_value', 'linux'),
        ('osx_value', 'osx')
    ]

    def get_choice_list(self):
        return self.choice_list

    def get_choice_list_lists(self):
        return self.choice_list_lists

    def get_choice_list_tuples(self):
        return self.choice_list_tuples

    def test_init(self):
        field = autocomplete.Select2ListChoiceField(
            choice_list=self.choice_list)
        self.assertCountEqual(
            field.choices,
            [(choice, choice) for choice in self.choice_list])

        field = autocomplete.Select2ListChoiceField(
            choice_list=self.get_choice_list)
        self.assertCountEqual(
            field.choices,
            [(choice, choice) for choice in self.choice_list])

    def test_init_lists(self):
        field = autocomplete.Select2ListChoiceField(
            choice_list=self.choice_list_lists)
        # choices are converted to tuples, not a big deal
        assert [*field.choices] == self.choice_list_tuples

        field = autocomplete.Select2ListChoiceField(
            choice_list=self.get_choice_list_lists)
        assert [*field.choices] == self.choice_list_tuples

    def test_init_tuples(self):
        field = autocomplete.Select2ListChoiceField(
            choice_list=self.choice_list_tuples)
        self.assertCountEqual(
            field.choices,
            [(value, text) for [value, text] in self.choice_list_tuples])

        field = autocomplete.Select2ListChoiceField(
            choice_list=self.get_choice_list_tuples)
        self.assertCountEqual(
            field.choices,
            [(value, text) for [value, text] in self.choice_list_tuples])


class Select2ListCreateChoiceFieldTest(test.TestCase):
    def test_validate(self):
        choice_list = ['windows', 'linux']
        field = autocomplete.Select2ListCreateChoiceField(
            choice_list=choice_list)

        # validate() should allow choice outside of choices...
        field.validate('osx')

        # but not empty.
        with self.assertRaises(ValidationError):
            field.validate('')
