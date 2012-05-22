import unittest

from django.db import models

import autocomplete_light
from autocomplete_light.templatetags import autocomplete_light_tags


class Foo(models.Model):
    pass


class Bar(autocomplete_light.ChannelBase):
    static_list = ('foo.js',)


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

    def test_register_channel_with_static(self):
        self.registry.register(Bar)
        self.assertIn('foo.js', self.registry.static_list)

    def test_unregister(self):
        self.registry.register(Bar)
        self.registry.unregister('Bar')
        self.assertEqual(self.registry.keys(), [])
        self.assertEqual(self.registry.static_list, [])

    def test_register_with_kwargs(self):
        self.registry.register(Foo, search_name='search_name')
        self.assertEqual(self.registry['FooChannel'].search_name,
            'search_name')

    def test_register_with_channel_and_kwargs(self):
        self.registry.register(Foo, Bar, search_name='search_name')
        self.assertEqual(self.registry['FooChannel'].search_name,
            'search_name')


class StaticTagTestCase(unittest.TestCase):
    def test_output(self):
        expected = ''.join([
            '<script src="/static/autocomplete_light/autocomplete.js" type="text/javascript"></script>',
            '<script src="/static/autocomplete_light/deck.js" type="text/javascript"></script>',
            '<link rel="stylesheet" type="text/css" href="/static/autocomplete_light/style.css"/>',
        ])
        output = autocomplete_light_tags.autocomplete_light_static()
        self.assertEqual(output, expected)
