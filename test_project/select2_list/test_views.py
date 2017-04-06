import json

from dal.autocomplete import Select2ListView

from django import test
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponseBadRequest

from .views import Select2ListViewAutocomplete


class Select2ListViewAutocompleteTest(Select2ListViewAutocomplete):
    def get_list(self):
        return ['WHEAT', 'WHy', 'why', 'WHEAT', 'Where', '2', 'Woot']


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

    def test_case_insensitive_results(self):
        def parse_results_from_response(http_response):
            return [
                word['text'] for word in
                json.loads(http_response.content.decode('utf8'))['results']
            ]

        view = Select2ListViewAutocompleteTest()
        view.q = 'Whe'

        expected_results = ['WHEAT', 'WHEAT', 'Where']
        incorrect_results = ['WHy', 'wheat', 'where', '', '2', 'Whe', 'WHERE']
        dal_results = parse_results_from_response(view.get(HttpRequest()))

        for word in expected_results:
            self.assertIn(word, dal_results)

        for word in incorrect_results:
            self.assertNotIn(word, dal_results)
