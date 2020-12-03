import json

from dal.autocomplete import Select2GroupListView, Select2ListView

from django import test
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponseBadRequest

from .views import (
    Select2ListViewAutocomplete,
    Select2ProvidedValueListViewAutocomplete,
)


class Select2ListViewAutocompleteTest(Select2ListViewAutocomplete):
    def get_list(self):
        return ['WHEAT', 'WHy', 'why', 'WHEAT', 'Where', '2', 'Woot']


class Select2GroupListViewAutocompleteTest(Select2GroupListView):
    def get_list(self):
        return [
            ('Country', ['France', 'Fiji', 'Finland', 'Switzerland']),
            'Pizza!',
            ('Foo', ['bar', 'BAZ']),
            ('tricky', ),
            ('more', 'tricky')
        ]


class Select2ProvidedValueListViewAutocompleteTest(
    Select2ProvidedValueListViewAutocomplete
):
    def get_list(self):
        return [
            ['WHEAT_value', 'WHEAT'],
            ['WHy_value', 'WHy'],
            ['why_value', 'why'],
            ['WHEAT_value', 'WHEAT'],
            ['Where_value', 'Where'],
            ['2_value', '2'],
            ['Woot_value', 'Woot']
        ]


class Select2GroupProvidedValueListViewAutocompleteTest(Select2GroupListView):
    def get_list(self):
        return [
            (
                ['Country_value', 'Country'],
                [
                    ['France_value', 'France'],
                    ['Fiji_value', 'Fiji'],
                    ['Finland_value', 'Finland'],
                    ['Switzerland_value', 'Switzerland']
                ]
            ),
            ([None, None], [['pizza_value', 'Pizza!']]),
            (['Foo_value', 'Foo'], [['bar_value', 'bar'], ['BAZ_value', 'BAZ']]),
            ([None, None], [['tricky_value', 'tricky']]),
            (['more_value', 'more'], [['tricky_value', 'tricky']])
        ]


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


class Select2ProvidedValueListViewAutocompleteCreateNone(
    Select2ProvidedValueListViewAutocomplete
):
    def create(self, text):
        return None


class Select2ProvidedValueListViewTest(test.TestCase):

    def test_empty(self):
        view = Select2ListView()
        self.assertEqual(view.get_list(), [])

    def test_post_fail(self):
        factory = test.RequestFactory()

        with self.assertRaises(ImproperlyConfigured):
            Select2ListView.as_view()(factory.post('/foo'))

        self.assertIsInstance(
            Select2ProvidedValueListViewAutocomplete.as_view()(factory.post('/foo')),
            HttpResponseBadRequest
        )

        self.assertIsInstance(
            Select2ProvidedValueListViewAutocompleteCreateNone.as_view()(
                factory.post('/foo', {'text': 'foo'})),
            HttpResponseBadRequest
        )

    def test_case_insensitive_results(self):
        def parse_results_from_response(http_response):
            return [
                word['text'] for word in
                json.loads(http_response.content.decode('utf8'))['results']
            ]

        view = Select2ProvidedValueListViewAutocompleteTest()
        view.q = 'Whe'

        expected_results = ['WHEAT', 'WHEAT', 'Where']
        incorrect_results = ['WHy', 'wheat', 'where', '', '2', 'Whe', 'WHERE']
        dal_results = parse_results_from_response(view.get(HttpRequest()))

        for word in expected_results:
            self.assertIn(word, dal_results)

        for word in incorrect_results:
            self.assertNotIn(word, dal_results)

    def test_case_insensitive_id_results(self):
        def parse_results_from_response(http_response):
            return [
                word['id'] for word in
                json.loads(http_response.content.decode('utf8'))['results']
            ]

        view = Select2ProvidedValueListViewAutocompleteTest()
        view.q = 'Whe'

        expected_results = ['WHEAT_value', 'WHEAT_value', 'Where_value']
        incorrect_results = [
            'WHEAT',
            'Where',
            'WHy',
            'wheat',
            'where',
            '',
            '2',
            'WHERE',
            'WHy_value',
            'wheat_value',
            'where_value',
            '2_value',
            'Whe_value',
            'WHERE_value'
        ]
        dal_results = parse_results_from_response(view.get(HttpRequest()))

        for word in expected_results:
            self.assertIn(word, dal_results)

        for word in incorrect_results:
            self.assertNotIn(word, dal_results)


class Select2GroupListViewTest(test.TestCase):
    def test_group_result(self):
        view = Select2GroupListViewAutocompleteTest()
        view.q = "baz"

        response = view.get(HttpRequest())
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode())["results"]

        self.assertEqual(len(results), 1)
        self.assertIn("children", results[0])
        self.assertEqual(len(results[0]["children"]), 1)
        self.assertEqual("BAZ", results[0]["children"][0]["text"])

    def test_string_in_group(self):
        view = Select2GroupListViewAutocompleteTest()
        view.q = "piz"

        response = view.get(HttpRequest())
        results = json.loads(response.content.decode())["results"]

        self.assertEqual(len(results), 1)
        self.assertEqual("Pizza!", results[0]["text"])

    def test_weird_in_group(self):
        view = Select2GroupListViewAutocompleteTest()
        view.q = "tricky"

        response = view.get(HttpRequest())
        results = json.loads(response.content.decode())["results"]

        self.assertEqual(len(results), 2)
        self.assertIn("children", results[1])
        self.assertEqual(len(results[1]["children"]), 1)
        self.assertEqual("tricky", results[1]["children"][0]["text"])


class Select2GroupProvidedValueListViewTest(test.TestCase):
    def test_group_result(self):
        view = Select2GroupProvidedValueListViewAutocompleteTest()
        view.q = "baz"

        response = view.get(HttpRequest())
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode())["results"]

        self.assertEqual(len(results), 1)
        self.assertIn("children", results[0])
        self.assertEqual(len(results[0]["children"]), 1)
        self.assertEqual("BAZ", results[0]["children"][0]["text"])
        self.assertEqual("BAZ_value", results[0]["children"][0]["id"])

    def test_string_in_group(self):
        view = Select2GroupProvidedValueListViewAutocompleteTest()
        view.q = "piz"

        response = view.get(HttpRequest())
        results = json.loads(response.content.decode())["results"]

        self.assertEqual(len(results), 1)
        self.assertEqual("Pizza!", results[0]["text"])
        self.assertEqual("pizza_value", results[0]["id"])

    def test_weird_in_group(self):
        view = Select2GroupProvidedValueListViewAutocompleteTest()
        view.q = "tricky"

        response = view.get(HttpRequest())
        results = json.loads(response.content.decode())["results"]

        self.assertEqual(len(results), 2)
        self.assertIn("children", results[1])
        self.assertEqual(len(results[1]["children"]), 1)
        self.assertEqual("tricky", results[1]["children"][0]["text"])
        self.assertEqual("tricky_value", results[1]["children"][0]["id"])
