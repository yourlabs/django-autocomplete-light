
import unittest
import autocomplete_light
from autocomplete_light import widgets


class FooComplete(autocomplete_light.AutocompleteModelBase):
    pass


class WidgetsTestCase(unittest.TestCase):

    def setUp(self):
        # stash/swap the registry, since WidgetBase directly accesses it
        self._original_registry = autocomplete_light.registry
        autocomplete_light.registry = autocomplete_light.AutocompleteRegistry()
        self.registry = autocomplete_light.registry

    def tearDown(self):
        autocomplete_light.registry = self._original_registry

    def test_lazy_autocomplete_init(self):
        try:
            widgets.WidgetBase('FooComplete')
        except autocomplete_light.AutocompleteNotRegistered:
            self.fail('WidgetBase initialization should not trigger registry '
                      'access')

    def test_lazy_autcomplete_access(self):
        widget = widgets.WidgetBase('FooComplete')
        try:
            widget.autocomplete
            self.fail('Should raise AutocompleteNotRegistered on unregistered '
                      'FooComplete')
        except autocomplete_light.AutocompleteNotRegistered:
            pass

        self.registry.register(FooComplete)
        self.assertIn('FooComplete', self.registry.keys())
        try:
            widget.autocomplete
        except autocomplete_light.AutocompleteNotRegistered:
            self.fail('widget.autocomplete access should not raise '
                      'AutocompleteNotRegistered')
