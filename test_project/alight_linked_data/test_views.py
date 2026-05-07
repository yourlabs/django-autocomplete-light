"""Tests for ViewMixin forward decoding via AlightQuerySetView."""

import json

from django import test
from django.urls import reverse
from django.utils.encoding import force_str

from .models import TModel
from .urls import AlightLinkedDataView


class ViewMixinTest(test.TestCase):
    """Forward parameter decoding raises appropriate errors."""

    def setUp(self):
        self.factory = test.RequestFactory()

    def test_no_forward_returns_200(self):
        request = self.factory.get(reverse('alight_linked_data'))
        response = AlightLinkedDataView.as_view(model=TModel)(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')

    def test_forward_not_dict_returns_400(self):
        request = self.factory.get(
            reverse('alight_linked_data') + '?forward=' + json.dumps([])
        )
        response = AlightLinkedDataView.as_view(model=TModel)(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(force_str(response.content), 'Not a JSON object')

    def test_forward_invalid_json_returns_400(self):
        request = self.factory.get(
            reverse('alight_linked_data') + '?forward={]'
        )
        response = AlightLinkedDataView.as_view(model=TModel)(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(force_str(response.content), 'Invalid JSON data')

    def test_invalid_method_returns_405(self):
        request = self.factory.put(reverse('alight_linked_data'))
        response = AlightLinkedDataView.as_view(model=TModel)(request)
        self.assertEqual(response.status_code, 405)

    def test_forward_filters_queryset(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user('lv_user', password='pw')
        TModel.objects.create(name='owned', owner=user)
        TModel.objects.create(name='unowned')

        forward = json.dumps({'owner': str(user.pk)})
        request = self.factory.get(
            reverse('alight_linked_data') + '?forward=' + forward
        )
        request.user = user
        response = AlightLinkedDataView.as_view(model=TModel)(request)
        content = force_str(response.content)
        self.assertIn('owned', content)
        self.assertNotIn('unowned', content)
