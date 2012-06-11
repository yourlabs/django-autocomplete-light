import unittest

from django.db import models

import autocomplete_light


class Foo(models.Model):
    pass


class Bar(autocomplete_light.ChannelBase):
    pass


class RegistryTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = autocomplete_light.ChannelRegistry()

    def test_register_model(self):
        self.registry.register(Foo)
        self.assertIn('FooChannel', self.registry.keys())

    def test_register_model_and_channel(self):
        self.registry.register(Foo, Bar)
        self.assertIn('FooChannel', self.registry.keys())

    def test_register_channel(self):
        self.registry.register(Bar)
        self.assertIn('Bar', self.registry.keys())

    def test_unregister(self):
        self.registry.register(Bar)
        self.registry.unregister('Bar')
        self.assertEqual(self.registry.keys(), [])

    def test_register_with_kwargs(self):
        self.registry.register(Foo, search_name='search_name')
        self.assertEqual(self.registry['FooChannel'].search_name,
            'search_name')

    def test_register_with_channel_and_kwargs(self):
        self.registry.register(Foo, Bar, search_name='search_name')
        self.assertEqual(self.registry['FooChannel'].search_name,
            'search_name')

    def test_register_with_custom_name(self):
        self.registry.register(Foo, Bar, channel_name='BarFoo')
        self.assertIn('BarFoo', self.registry.keys())
        self.assertEqual(self.registry['BarFoo'].__name__, 'BarFoo')
