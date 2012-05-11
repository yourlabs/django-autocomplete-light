import unittest

from autocomplete_light.templatetags import autocomplete_light_tags


class StaticTagTestCase(unittest.TestCase):
    def test_output(self):
        expected = ''.join([
            '<script src="/static/autocomplete_light/autocomplete.js" type="text/javascript"></script>',
            '<script src="/static/autocomplete_light/deck.js" type="text/javascript"></script>',
            '<link rel="stylesheet" type="text/css" href="/static/autocomplete_light/style.css" />',
        ])
        output = autocomplete_light_tags.autocomplete_light_static()
        self.assertEqual(output, expected)
