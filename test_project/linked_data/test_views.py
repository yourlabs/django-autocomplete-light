"""Test the base autocomplete view."""

import json

from django import test
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.utils.encoding import force_text

from .models import TModel
from .urls import LinkedDataView


class ViewMixinTest(test.TestCase):  # noqa
    """TestCase for ViewMixin data decoding."""

    def setUp(self):
        self.factory = test.RequestFactory()

    def test_no_data(self):
        request = self.factory.get(reverse('linked_data'))

        response = LinkedDataView.as_view(model=TModel)(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content),
                             '{"results": [], "pagination": {"more": false}}')

    def test_not_dict(self):
        request = self.factory.get(
            reverse('linked_data') + '?forward=' + json.dumps('[]')
        )

        response = LinkedDataView.as_view(model=TModel)(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(force_text(response.content), 'Not a JSON object')

    def test_invalid_json(self):
        request = self.factory.get(
            reverse('linked_data') + '?forward={]'
        )

        response = LinkedDataView.as_view(model=TModel)(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(force_text(response.content), 'Invalid JSON data')

    def test_invalid_method(self):
        request = self.factory.put(reverse('linked_data'))

        response = LinkedDataView.as_view(model=TModel)(request)
        self.assertEqual(response.status_code, 405)
