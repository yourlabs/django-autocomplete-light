"""Unit tests for dal_alight_queryset_sequence views."""

import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import RequestFactory, TestCase

from dal_alight_queryset_sequence.views import (
    AlightQuerySetSequenceAutoView,
    AlightQuerySetSequenceView,
)

from .models import TModel

User = get_user_model()


def _make_view(model_choice):
    """Return a concrete AlightQuerySetSequenceAutoView subclass."""
    return type(
        'AutoView', (AlightQuerySetSequenceAutoView,), {'model_choice': model_choice}
    )


class AlightQuerySetSequenceViewTest(TestCase):
    """AlightQuerySetSequenceView.render_to_response groups results by model."""

    def setUp(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='alpha_group')
        self.tmodel = TModel.objects.create(name='beta_tmodel')

    def _get(self, q=''):
        from queryset_sequence import QuerySetSequence
        view = AlightQuerySetSequenceView.as_view(
            queryset=QuerySetSequence(
                Group.objects.all(),
                TModel.objects.filter(pk=self.tmodel.pk),
            )
        )
        request = self.factory.get('/', {'q': q})
        request.user = User()
        return view(request)

    def test_content_type_is_html(self):
        r = self._get()
        self.assertEqual(r['Content-Type'], 'text/html; charset=utf-8')

    def test_group_headers_rendered_for_each_model_type(self):
        r = self._get()
        content = r.content.decode()
        self.assertIn('autocomplete-light-group', content)
        # Two distinct model types → two group headers.
        self.assertEqual(content.count('autocomplete-light-group'), 2)

    def test_results_have_data_value(self):
        r = self._get()
        self.assertIn('data-value=', r.content.decode())

    def test_filtering_returns_matching_results(self):
        r = self._get(q='alpha')
        content = r.content.decode()
        self.assertIn('alpha_group', content)
        self.assertNotIn('beta_tmodel', content)

    def test_group_label_is_verbose_name(self):
        r = self._get()
        content = r.content.decode()
        # Group model verbose name is 'group'
        self.assertIn('group', content.lower())


class AlightQuerySetSequenceAutoViewTest(TestCase):
    """AlightQuerySetSequenceAutoView.get_queryset applies forwarding."""

    def setUp(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='gamma_group')

    def _get(self, view_cls, q='', forward=None):
        params = {'q': q}
        if forward:
            params['forward'] = json.dumps(forward)
        request = self.factory.get('/', params)
        request.user = User()
        return view_cls.as_view()(request)

    def test_two_element_model_args_no_error(self):
        view_cls = _make_view([(Group, 'name')])
        r = self._get(view_cls, q='gamma')
        self.assertEqual(r.status_code, 200)
        self.assertIn('gamma_group', r.content.decode())

    def test_three_element_model_args_with_empty_forward_list(self):
        view_cls = _make_view([(Group, 'name', [])])
        r = self._get(view_cls, q='gamma')
        self.assertEqual(r.status_code, 200)

    def test_forward_filter_applied(self):
        Group.objects.create(name='delta_group')
        view_cls = _make_view([
            (Group, 'name', [('name', 'name')]),
        ])
        r = self._get(view_cls, q='', forward={'name': 'gamma'})
        content = r.content.decode()
        self.assertIn('gamma_group', content)
        self.assertNotIn('delta_group', content)

    def test_forward_field_not_in_forwarded_skipped(self):
        # No 'city' key in forwarded → filter skipped, all results returned.
        view_cls = _make_view([
            (Group, 'name', [('city', 'name')]),
        ])
        r = self._get(view_cls, q='gamma')
        self.assertEqual(r.status_code, 200)
        self.assertIn('gamma_group', r.content.decode())
