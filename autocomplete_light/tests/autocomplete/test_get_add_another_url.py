try:
    from unittest import mock
except ImportError:  # python2
    import mock

import autocomplete_light.shortcuts as autocomplete_light
from autocomplete_light.compat import urls, url
from django import test

try:
    from django.test import override_settings
except ImportError:
    override_settings = None

urlpatterns = urls([
    url(r'nokwarg/$', mock.Mock, name='test_nokwarg'),
    url(r'onekwarg/(?P<param>\w+)/$', mock.Mock, name='test_onekwarg'),
])


class GetAddAnotherUrlTestCase(test.TestCase):

    def generate_url(self, name, kwargs=None):
        class TestAutocomplete(autocomplete_light.AutocompleteBase):
            add_another_url_name = name
            add_another_url_kwargs = kwargs

        return TestAutocomplete().get_add_another_url()

    def test_no_kwargs(self):
        self.assertEquals(self.generate_url('test_nokwarg'),
                          '/nokwarg/?_popup=1')

    def test_with_kwargs(self):
        self.assertEquals(self.generate_url('test_onekwarg', {'param': 'bar'}),
                          '/onekwarg/bar/?_popup=1')

if override_settings:
    GetAddAnotherUrlTestCase = override_settings(ROOT_URLCONF='autocomplete_light.tests.autocomplete.test_get_add_another_url')(GetAddAnotherUrlTestCase)
else:
    GetAddAnotherUrlTestCase.urls = 'autocomplete_light.tests.autocomplete.test_get_add_another_url'
