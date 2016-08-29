from dal.autocomplete import Select2ListView

from django import test
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseBadRequest

from .views import Select2ListViewAutocomplete


class Select2ListViewAutocompleteCreateNone(Select2ListViewAutocomplete):
    def create(self, text):
        return None


class Select2ListViewTest(test.TestCase):

    def test_empty(self):
        view = Select2ListView()
        self.assertEqual(view.get_list(), [])

    def test_post_fail(self):
        factory = test.RequestFactory()

        with self.assertRaises(ImproperlyConfigured):
            Select2ListView.as_view()(factory.post('/foo'))

        self.assertIsInstance(
            Select2ListViewAutocomplete.as_view()(factory.post('/foo')),
            HttpResponseBadRequest
        )

        self.assertIsInstance(
            Select2ListViewAutocompleteCreateNone.as_view()(
                factory.post('/foo', {'text': 'foo'})),
            HttpResponseBadRequest
        )
