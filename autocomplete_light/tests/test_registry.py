import unittest

import autocomplete_light.shortcuts as autocomplete_light
import django
from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase


class Noname(models.Model):
    number = models.CharField(max_length=100)


class Foo(models.Model):
    name = models.CharField(max_length=100)


class Bar(autocomplete_light.AutocompleteModelBase):
    pass


class Generic(autocomplete_light.AutocompleteGenericBase):
    choices = (
        User.objects.all(),
    )
    search_fields = (
        ('username',),
    )


class RegistryTestCase(TestCase):
    def setUp(self):
        self.registry = autocomplete_light.AutocompleteRegistry()

    def test_register_model(self):
        self.registry.register(Foo)
        self.assertIn('FooAutocomplete', self.registry.keys())

    def test_register_model_and_autocomplete(self):
        self.registry.register(Foo, Bar)
        self.assertIn('FooBar', self.registry.keys())

    def test_register_autocomplete(self):
        self.registry.register(Bar)
        self.assertIn('Bar', self.registry.keys())

    def test_unregister(self):
        self.registry.register(Bar)
        self.registry.unregister('Bar')
        self.assertEqual(list(self.registry.keys()), [])

    def test_register_with_kwargs(self):
        choices = ['foo']
        self.registry.register(Foo, search_name='search_name', choices=choices)
        self.assertEqual(self.registry['FooAutocomplete'].search_name,
            'search_name')
        self.assertEqual(self.registry['FooAutocomplete'].choices, choices)

    def test_register_with_custom_autocomplete_model_base(self):
        class NewBase(autocomplete_light.AutocompleteModelBase):
            new_base = True

        self.registry.autocomplete_model_base = NewBase
        self.registry.register(Foo)
        self.assertEqual(NewBase, self.registry['FooAutocomplete'].__base__)
        self.assertTrue(self.registry['FooAutocomplete'].new_base)

    def test_register_with_autocomplete_and_kwargs(self):
        self.registry.register(Foo, Bar, search_name='search_name')
        self.assertEqual(self.registry['FooBar'].search_name,
            'search_name')

    def test_register_with_custom_name(self):
        self.registry.register(Foo, Bar, name='BarFoo')
        self.assertIn('BarFoo', self.registry.keys())
        self.assertEqual(self.registry['BarFoo'].__name__, 'BarFoo')

    def test_register_no_name_fail(self):
        try:
            self.registry.register(Noname)
            self.fail('Should raise an exception when registering noname')
        except:
            pass

    def test_register_no_name_pass(self):
        self.registry.register(Noname, search_fields=('number',))

    def test_register_generic_with_custom_name(self):
        self.registry.register(Generic, name='foo')
        self.assertTrue('foo' in self.registry.keys())

    def test_raise_AutocompleteNotRegistered(self):
        try:
            self.registry['NotRegistered']
            self.fail('Should raise AutocompleteNotRegistered')
        except autocomplete_light.AutocompleteNotRegistered:
            pass

    def test_raise_NoGenericAutocompleteRegistered(self):
        self.assertRaises(autocomplete_light.NoGenericAutocompleteRegistered,
                          self.registry.autocomplete_for_generic)

    def test_autocomplete_for_model(self):
        class FirstAutocomplete(autocomplete_light.AutocompleteModelBase):
            pass

        class SecondAutocomplete(autocomplete_light.AutocompleteModelBase):
            pass

        self.registry.register(Foo, FirstAutocomplete)
        self.registry.register(Foo, SecondAutocomplete)

        self.assertTrue(issubclass(
            self.registry.autocomplete_for_model(Foo), FirstAutocomplete))

    def test_autocomplete_for_generic(self):
        class FirstAutocomplete(Generic):
            pass

        class SecondAutocomplete(Generic):
            pass

        self.registry.register(FirstAutocomplete)
        self.registry.register(SecondAutocomplete)

        self.assertTrue(issubclass(
            self.registry.autocomplete_for_generic(), FirstAutocomplete))

    def test_register_model_as_string_app_name_dot_model_name(self):
        self.registry.register('auth.User')
        self.assertIn('UserAutocomplete', self.registry.keys())

    def test_register_model_as_string_invalid_app_name_dot_model_name(self):
        try:
            self.registry.register('invalid_appname.User')
            self.fail('Should raise an exception because "LookupError: No installed app with label invalid_appname"')
        except LookupError:
            pass

    def test_register_model_as_string_app_name_dot_invalid_model_name(self):
        try:
            self.registry.register('django.contrib.auth.models.UserWrong')
            self.fail(
                'Should raise an exception because "ImportError: Module '
                '"django.contrib.auth.models" does not define a \"UserWrong\" attribute/class"')
        except ImportError:
            pass

    def test_register_model_as_string_full_dot_path_to_model(self):
        self.registry.register('django.contrib.auth.models.User')
        self.assertIn('UserAutocomplete', self.registry.keys())

    def test_register_model_as_string_full_dot_path_to_non_model(self):
        try:
            self.registry.register('django.contrib.auth.forms.UserCreationForm')
            self.fail('Should raise an exception NonDjangoModelSubclassException because '
                      'UserCreationForm not is subclass of django Model')
        except autocomplete_light.NonDjangoModelSubclassException:
            pass

    def test_register_model_as_string_invalid_full_dot_path_to_non_model(self):
        try:
            self.registry.register('django.invalid_path.UserCreationForm')
            self.fail('Should raise an exception because is invalid dot path to Model')
        except ImportError:
            pass


class RegistryGetAutocompleteFromArgTestCase(TestCase):
    def setUp(self):
        self.registry = autocomplete_light.AutocompleteRegistry()
        self.registry.register(Foo)
        self.registry.register(Generic)

    def test_from_string(self):
        a = self.registry.get_autocomplete_from_arg('FooAutocomplete')
        self.assertEqual(a.model, Foo)

    def test_from_model(self):
        a = self.registry.get_autocomplete_from_arg(Foo)
        self.assertEqual(a.model, Foo)

    def test_from_model_instance(self):
        a = self.registry.get_autocomplete_from_arg(Foo())
        self.assertEqual(a.model, Foo)

    def test_from_autocomplete_instance(self):
        a = self.registry.get_autocomplete_from_arg(Generic)
        self.assertEqual(a, Generic)

    def test_default_generic(self):
        a = self.registry.get_autocomplete_from_arg()
        self.assertTrue(issubclass(a, Generic))

    def test_model_picked_up_from_autocomplete_class_model(self):
        # GitHub issue #313
        class TestModel(models.Model):
            name = models.CharField(max_length=100)

        class XAutocomplete(autocomplete_light.AutocompleteModelBase):
            model = TestModel

        self.registry.register(XAutocomplete)
        result = self.registry.get_autocomplete_from_arg(TestModel)

        assert result
        assert issubclass(result, XAutocomplete)

    def test_model_picked_up_from_autocomplete_class_choices_model(self):
        class TestModel(models.Model):
            name = models.CharField(max_length=100)

        class YAutocomplete(autocomplete_light.AutocompleteModelBase):
            choices = TestModel.objects.all()

        self.registry.register(YAutocomplete)
        result = self.registry.get_autocomplete_from_arg(TestModel)

        assert result
        assert issubclass(result, YAutocomplete)

    def test_registering_autocomplete_without_model_name_as_prefix(self):
        class TestModel(models.Model):
            name = models.CharField(max_length=100)

        class Base(autocomplete_light.AutocompleteModelBase):
            pass

        class BarAutocomplete(Base):
            model = TestModel
            choices = TestModel.objects.all()

        self.registry.register(BarAutocomplete)
        assert 'BarAutocomplete' in self.registry
        result = self.registry.get_autocomplete_from_arg(TestModel)
        assert result
        assert issubclass(result, BarAutocomplete)


@unittest.skipIf(django.VERSION < (1, 7), 'require django 1.7')
class AppConfigSupportTestCase(TestCase):
    def test_appconfig_with_registry_file(self):
        self.assertIsInstance(autocomplete_light.registry['AppConfigWithRegistryAutocomplete'](),
                             autocomplete_light.AutocompleteListBase)

    def test_appconfig_without_registry_file(self):
        self.assertIsInstance(autocomplete_light.registry['AppConfigWithoutRegistryAutocomplete'](),
                              autocomplete_light.AutocompleteListBase)
