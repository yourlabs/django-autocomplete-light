import autocomplete_light.shortcuts as autocomplete_light
from django.test import TestCase
from lxml.cssselect import CSSSelector
from lxml.html import etree

from ..example_apps.basic.models import FkModel

try:
    from unittest import mock
except ImportError:  # python2
    import mock





class LazyAutocomplete(autocomplete_light.AutocompleteModelBase):
    pass


class WidgetBaseMixin(object):
    widget_class = autocomplete_light.WidgetBase
    fixtures = ['security_test']

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

    def test_widget_js_attributes_deprecation(self):
        with self.assertRaises(PendingDeprecationWarning):
            self.widget_class(widget_js_attributes={'foo': 'bar'})

    def test_autocomplete_js_attributes_deprecation(self):
        with self.assertRaises(PendingDeprecationWarning):
            self.widget_class(autocomplete_js_attributes={'foo': 'bar'})

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
                'attrs': mock.ANY,
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
                'attrs': mock.ANY,
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

        # This was originally masked from the test suite because method
        # definition was repeated
        widget = self.widget_class('FkModelAutocomplete',
            widget_attrs={'data-widget-foo': 'bar', 'class':'foobar'})
        html = widget.render('somewidget', None)
        et = etree.fromstring(html)
        self.assertEquals(et.attrib['data-widget-foo'], 'bar')
        self.assertIn('foobar', et.attrib['class'])
        self.assertIn('autocomplete-light-widget', et.attrib['class'])

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

    def test_value_out_of_queryset(self):
        widget = self.widget_class('ItemAutocomplete')
        html = widget.render('somewidget', [1, 2])
        span = etree.fromstring(html)

        choices = CSSSelector('[data-value]')(span)

        self.assertEqual(len(choices), 1)
        self.assertEqual(int(choices[0].attrib['data-value']), 1)

class ChoiceWidgetTestCase(WidgetBaseMixin, TestCase):
    widget_class = autocomplete_light.ChoiceWidget

    def test_attrs_copy_class(self):
        widget = self.widget_class('A2')
        html = widget.render('taggit', value='oky')
        et = etree.XML(html)
        self.assertTrue(et.find('input').get('data-class-defined'), '1')

    def test_attrs_copy_init(self):
        widget = self.widget_class('A2')
        html = widget.render('taggit', value='oky')
        et = etree.XML(html)

        self.assertTrue(et.find('input').get('data-init-defined'), '2')


class MultipleChoiceWidgetTestCase(WidgetBaseMixin, TestCase):
    widget_class = autocomplete_light.MultipleChoiceWidget


class TextWidgetTestCase(WidgetBaseMixin, TestCase):
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

    def test_value_out_of_queryset(self):
        pass  # no queryset for text widget

    def test_widget_attrs_copy(self):
        # Test case for GH269
        widget = self.widget_class('B')
        html = widget.render('taggit', value='Cued Speech, languages')
        et = etree.XML(html)
        self.assertTrue('value' in et.attrib)

        html = widget.render('taggit', None)
        et = etree.XML(html)
        self.assertFalse('value' in et.attrib)

    def test_attrs_copy_class(self):
        widget = self.widget_class('B2')
        html = widget.render('taggit', value='oky')
        et = etree.XML(html)
        self.assertTrue('data-class-defined' in et.attrib)

    def test_attrs_copy_init(self):
        widget = self.widget_class('B2')
        html = widget.render('taggit', value='oky')
        et = etree.XML(html)
        self.assertTrue('data-init-defined' in et.attrib)
