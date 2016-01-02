"""Test the base widget."""

from dal.widgets import Select

from django import forms
from django import http
from django import test
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils import six

import mock


urlpatterns = [
    url(
        r'^test-url/$',
        mock.Mock(),
        name='test_url'
    ),
]


@override_settings(ROOT_URLCONF='tests.test_widgets')
class SelectTest(test.TestCase):  # noqa
    """Test case for the Select widget."""

    def test_widget_renders_only_selected_with_url(self):
        """Assert that it won't render unselected choices, if given a url."""
        class Form(forms.Form):
            test = forms.ChoiceField(
                choices=[(i, 'label for %s' % i) for i in range(0, 100)],
                widget=Select(url=reverse('test_url'))
            )

        form = Form(http.QueryDict('test=4'))
        expected = '''
<select data-autocomplete-light-url="/test-url/" id="id_test" name="test">
<option value="4" selected="selected">label for 4</option>
</select>
        '''.strip()

        self.assertEquals(six.text_type(form['test'].as_widget()), expected)
