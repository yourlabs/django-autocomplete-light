"""Test the base widget."""

from dal.autocomplete import Select2
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
                widget=Select(url=reverse('test_url')),
                required=False
            )

        form = Form(http.QueryDict('test=4'))
        expected = '''
<select data-autocomplete-light-url="/test-url/" id="id_test" name="test">
<option value="4" selected="selected">label for 4</option>
</select>
        '''.strip()

        self.assertEquals(six.text_type(form['test'].as_widget()), expected)


@override_settings(ROOT_URLCONF='tests.test_widgets')
class Select2Test(test.TestCase):  # noqa
    """Test case for the Select2 widget."""

    def test_widget_renders_empty_option_with_placeholder_without_url(self):
        """Assert that it renders an empty option, if not given a url."""
        class Form(forms.Form):
            test = forms.ChoiceField(
                choices=[(1, "A")],
                widget=Select2(attrs={
                    "data-placeholder": "Some placeholder",
                }),
                required=False
            )

        form = Form(http.QueryDict())
        expected = '''
<select data-autocomplete-light-function="select2"\
 data-placeholder="Some placeholder" id="id_test" name="test">
<option value="" selected="selected"></option>
<option value="1">A</option>
</select>
        '''.strip()
        observed = six.text_type(form['test'].as_widget())

        self.assertEquals(observed, expected)

    def test_widget_no_empty_option_without_placeholder_without_url(self):
        """Assert that it renders an empty option, if not given a url."""
        class Form(forms.Form):
            test = forms.ChoiceField(
                choices=[(1, "A")],
                widget=Select2(),
                required=False
            )

        form = Form(http.QueryDict())
        expected = '''
<select data-autocomplete-light-function="select2" id="id_test" name="test">
<option value="1">A</option>
</select>
        '''.strip()
        observed = six.text_type(form['test'].as_widget())

        self.assertEquals(observed, expected)

        form = Form(http.QueryDict('test=1'))
        expected = '''
<select data-autocomplete-light-function="select2" id="id_test" name="test">
<option value="1" selected="selected">A</option>
</select>
        '''.strip()
        observed = six.text_type(form['test'].as_widget())

        self.assertEquals(observed, expected)
