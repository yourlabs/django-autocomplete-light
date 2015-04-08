from __future__ import unicode_literals

import autocomplete_light.shortcuts as autocomplete_light
import six
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory, TestCase
from django.utils.encoding import force_text

try:
    from unittest.mock import Mock, MagicMock, patch
except ImportError:  # python2
    from mock import Mock, MagicMock, patch

try:
    from django.contrib.auth import get_user_model
except ImportError:
    # Django 1.4
    from django.contrib.auth.models import User
else:
    User = get_user_model()



class RegistryViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        u = User.objects.create(is_staff=True, username='u', is_active=True)
        u.set_password('p')
        u.save()

        u = User.objects.create(is_staff=True, username='su', is_active=True,
                is_superuser=True)
        u.set_password('p')
        u.save()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def setUp(self):
        self.admin = Client()
        self.admin.login(username='u', password='p')

        self.superuser = Client()
        self.superuser.login(username='su', password='p')

        self.anonymous = Client()

        self.registry = autocomplete_light.AutocompleteRegistry()

    def test_requires_superuser(self):
        response = self.anonymous.get(reverse('autocomplete_light_registry'))
        self.assertEqual(response.status_code, 403)

        response = self.admin.get(reverse('autocomplete_light_registry'))
        self.assertEqual(response.status_code, 403)

        response = self.superuser.get(reverse('autocomplete_light_registry'))
        self.assertEqual(response.status_code, 200)

    def test_get_context_data(self):
        response = self.superuser.get(reverse('autocomplete_light_registry'))

        self.assertEqual(response.context['registry'],
                autocomplete_light.registry)
        self.assertEqual(response.context['registry_items'],
                autocomplete_light.registry.items())

    def test_output(self):
        self.registry.register(User)

        with patch('autocomplete_light.views.RegistryView.get_registry') as p:
            p.return_value = self.registry

            response = self.superuser.get(reverse('autocomplete_light_registry'))

        self.assertIn('List of your 1 registered autocompletes', force_text(response.content))
        self.assertIn(reverse('autocomplete_light_autocomplete',
            args=['UserAutocomplete']), force_text(response.content))


class AutocompleteViewTestCase(TestCase):
    def test_404(self):
        c = Client()
        response = c.get(reverse('autocomplete_light_autocomplete',
            args=['Foo']))
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        registry = MagicMock()
        registry.__getitem__.return_value.return_value.autocomplete_html.return_value = 'foo'

        with patch('autocomplete_light.views.AutocompleteView.get_registry') as p:
            p.return_value = registry

            request = RequestFactory().get(
                reverse('autocomplete_light_autocomplete', args=['UserAutocomplete']))

            response = autocomplete_light.AutocompleteView.as_view()(request,
                autocomplete='UserAutocomplete')

        registry.__getitem__.assert_called_with('UserAutocomplete')
        registry.__getitem__.return_value.assert_called_with(request=request)
        registry.__getitem__.return_value.return_value.autocomplete_html.assert_called_with()

        self.assertIn('foo', force_text(response.content))

    def test_post(self):
        registry = MagicMock()

        with patch('autocomplete_light.views.AutocompleteView.get_registry') as p:
            p.return_value = registry

            request = RequestFactory().post(
                reverse('autocomplete_light_autocomplete', args=['UserAutocomplete']))

            autocomplete_light.AutocompleteView.as_view()(request,
                autocomplete='UserAutocomplete')

        registry.__getitem__.assert_called_with('UserAutocomplete')
        registry.__getitem__.return_value.assert_called_with()

        registry.__getitem__.return_value.return_value.post.assert_called_with(request,
                autocomplete='UserAutocomplete')


class CreateViewTestCase(TestCase):
    def test_respond_script(self):
        view = autocomplete_light.CreateView()
        class FakeModel(object):
            pk = 5
            def __str__(self):
                return 'abc "yoo"'

        view.object = FakeModel()
        output = view.respond_script()
        expected = '''
        <script type="text/javascript">opener.dismissAddAnotherPopup( window, "5", "abc \\"yoo\\"" );</script>
        '''
        self.assertEqual(force_text(expected.strip()),
                force_text(output.content.strip()))
        self.assertEqual(output.status_code, 201)

    def test_is_popup(self):
        view = autocomplete_light.CreateView()

        request = RequestFactory().get(
            reverse('autocomplete_light_autocomplete', args=['UserAutocomplete']))
        view.request = request
        self.assertFalse(view.is_popup())

        request = RequestFactory().get(
            reverse('autocomplete_light_autocomplete', args=['UserAutocomplete']) + '?_popup=1')
        view.request = request
        self.assertTrue(view.is_popup())

    def test_form_valid(self):
        form = Mock()

        if six.PY3:
            to_patch = 'builtins.super'
        else:
            to_patch = '__builtin__.super'

        with patch(to_patch) as patcher:
            patcher.is_local = True

            view = autocomplete_light.CreateView()
            view.request = Mock()
            view.request.GET.get.return_value = False
            view.object = Mock()
            response = view.form_valid(form)

            # Assert that the parent's response was returned
            self.assertEqual(patcher().form_valid(), response)

            # as popup,
            view.request.GET.get.return_value = '1'
            view.respond_script = lambda: 'foo'
            response = view.form_valid(form)

            # assert that the response contains the script
            self.assertEqual('foo', response)
            self.assertEqual(view.success_url, '/')
