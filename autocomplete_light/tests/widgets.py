import re
import unittest

from lxml import etree
from lxml.cssselect import CSSSelector

try:
    from unittest import mock
except ImportError:  # python2
    import mock

from django import template
import autocomplete_light

from ..example_apps.basic.models import FkModel


class LazyAutocomplete(autocomplete_light.AutocompleteModelBase):
    pass


class WidgetBaseTestCase(unittest.TestCase):
    widget_class = autocomplete_light.WidgetBase

    def autocomplete_input(self, et):
        return CSSSelector('input.autocomplete')(et)[0]

    def test_init_with_registry(self):
        registry = autocomplete_light.AutocompleteRegistry()
        registry.register(FkModel, name='TestAutocomplete')

        widget = self.widget_class('TestAutocomplete', registry=registry)
        self.assertEqual(widget.autocomplete.__name__, 'TestAutocomplete')

    def test_init_without_registry(self):
        widget = self.widget_class('FkModelAutocomplete')
        self.assertEqual(widget.autocomplete.model, FkModel)

    def test_widget_data_attributes(self):
        widget = self.widget_class('FkModelAutocomplete',
            widget_attrs={'data-widget-foo': 'bar', 'class':'foobar'})
        html = widget.render('somewidget', None)

    def test_widget_js_attributes_deprecation(self):
        with self.assertRaises(PendingDeprecationWarning) as context:
            widget = self.widget_class(widget_js_attributes={'foo': 'bar'})

    def test_autocomplete_js_attributes_deprecation(self):
        with self.assertRaises(PendingDeprecationWarning) as context:
            widget = self.widget_class(autocomplete_js_attributes={'foo': 'bar'})

    @mock.patch('autocomplete_light.widgets.render_to_string')
    def test_widget_template(self, render_to_string):
        widget = self.widget_class('FkModelAutocomplete',
            widget_template='foo.html')
        widget.render('somewidget', None)
        render_to_string.assert_called_with('foo.html', mock.ANY)

    @mock.patch('autocomplete_light.widgets.render_to_string')
    def test_autocomplete_widget_template(self, render_to_string):
        class Autocomplete(autocomplete_light.AutocompleteListBase):
            widget_template='bar.html'
            choices = ['a', 'b']

        widget = self.widget_class(Autocomplete)
        widget.render('somewidget', [])
        render_to_string.assert_called_with('bar.html', mock.ANY)

    @mock.patch('autocomplete_light.widgets.render_to_string')
    def test_base_context(self, render_to_string):
        widget = self.widget_class('FkModelAutocomplete')
        widget.render('somewidget', None)
        render_to_string.assert_called_with(
            'autocomplete_light/widget.html', {
                'widget': widget,
                'choices': mock.ANY,
                'autocomplete': mock.ANY,
                'input_attrs': mock.ANY,
                'widget_attrs': mock.ANY,
                'name': 'somewidget',
                'values': [],
            })

    @mock.patch('autocomplete_light.widgets.render_to_string')
    def test_extra_context(self, render_to_string):
        widget = self.widget_class('FkModelAutocomplete',
                                   extra_context={'foo': 'bar'})

        widget.render('somewidget', None)

        render_to_string.assert_called_with(
            'autocomplete_light/widget.html', {
                'widget': widget,
                'choices': mock.ANY,
                'autocomplete': mock.ANY,
                'input_attrs': mock.ANY,
                'widget_attrs': mock.ANY,
                'name': 'somewidget',
                'values': [],
                'foo': 'bar',
            })

    def test_input_placeholder_attr(self):
        widget = self.widget_class('FkModelAutocomplete',
                                   attrs={'placeholder': 'foo'})
        html = widget.render('somewidget', None)
        et = etree.XML(html)

        self.assertEqual(self.autocomplete_input(et).attrib['placeholder'],
                         'foo')

    def test_widget_attrs(self):
        widget = self.widget_class('FkModelAutocomplete',
                                   widget_attrs={'class': 'foo'})
        html = widget.render('somewidget', None)
        et = etree.XML(html)

        self.assertIn('foo', et.attrib['class'])

    def test_lazy_autocomplete_init(self):
        registry = autocomplete_light.AutocompleteRegistry()

        try:
            self.widget_class('LazyAutocomplete', registry=registry)
        except autocomplete_light.AutocompleteNotRegistered:
            self.fail('WidgetBase initialization should not trigger registry '
                      'access')

    def test_lazy_autcomplete_access(self):
        registry = autocomplete_light.AutocompleteRegistry()

        widget = self.widget_class('LazyAutocomplete', registry=registry)

        try:
            widget.autocomplete
            self.fail('Should raise AutocompleteNotRegistered on unregistered '
                      'LazyAutocomplete')
        except autocomplete_light.AutocompleteNotRegistered:
            pass

        registry.register(LazyAutocomplete)
        self.assertIn('LazyAutocomplete', registry.keys())

        try:
            widget.autocomplete
        except autocomplete_light.AutocompleteNotRegistered:
            self.fail('widget.autocomplete access should not raise '
                      'AutocompleteNotRegistered')

class ChoiceWidgetTestCase(WidgetBaseTestCase):
    widget_class = autocomplete_light.ChoiceWidget


class MultipleChoiceWidgetTestCase(WidgetBaseTestCase):
    widget_class = autocomplete_light.MultipleChoiceWidget


class TextWidgetTestCase(WidgetBaseTestCase):
    widget_class = autocomplete_light.TextWidget

    def autocomplete_input(self, et):
        return et

    def test_extra_context(self):
        pass  # no template for TextWidget

    def test_widget_template(self):
        pass  # no template for TextWidget

    def test_base_context(self):
        pass  # no template for TextWidget

    def test_autocomplete_widget_template(self):
        pass  # no template for TextWidget

    def test_widget_attrs(self):
        pass  # no widget_attrs for TextWidget
