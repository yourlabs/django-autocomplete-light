import json

from dal import autocomplete

from django import test
from django.contrib.auth.models import Group


class Select2QuerySetSequenceViewTestCase(test.TestCase):
    def setUp(self):
        self.expected = {
            'pagination': {
                'more': False
            },
            'results': []
        }

    @classmethod
    def setUpClass(cls):
        for i in range(0, 3):
            Group.objects.create(name='ViewTestCase%s' % i)

        cls.request = test.RequestFactory().get('?q=foo')
        super(Select2QuerySetSequenceViewTestCase, cls).setUpClass()

    def get_view(self, **kwargs):
        view = autocomplete.Select2QuerySetSequenceView(
            queryset=autocomplete.QuerySetSequence(
                Group.objects.all(),
            ),
            paginate_by=2,
            **kwargs
        )
        view.request = self.request
        return view

    def get_view_response(self, **view_kwargs):
        return self.get_view(**view_kwargs).dispatch(self.request)

    def get_view_response_json(self, **view_kwargs):
        return json.loads(self.get_view_response(**view_kwargs).content)

    def test_get(self):
        result = self.get_view_response_json()
        assert self.expected == result

    def test_get_with_create_field(self):
        self.expected['results'].append({
            'text': 'Create "foo"',
            'id': 'foo',
            'create_id': True
        })
        result = self.get_view_response_json(create_field='name')
        assert self.expected == result
