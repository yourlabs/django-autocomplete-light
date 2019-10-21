"""Test the base widget."""

from dal.autocomplete import Select2
from dal.widgets import Select, WidgetMixin

from dal_select2 import widgets as select2_widget

import django
from django import forms
from django import http
from django import test
from django.conf.urls import url
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.test.utils import override_settings

import mock

import six


urlpatterns = [
    url(
        r'^test-url/$',
        mock.Mock(),
        name='test_url'
    ),
]


def selected_tag():
    return 'selected="selected"' if django.VERSION < (1, 11) else 'selected'


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
<option value="4" %s>label for 4</option>
</select>
        '''.strip() % selected_tag()

        self.assertHTMLEqual(six.text_type(form['test'].as_widget()), expected)


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
 data-autocomplete-light-language="en"\
 data-placeholder="Some placeholder" id="id_test" name="test">
<option value="" %s></option>
<option value="1">A</option>
</select>
        '''.strip() % selected_tag()
        observed = six.text_type(form['test'].as_widget())

        self.assertHTMLEqual(observed, expected)

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
<select data-autocomplete-light-function="select2"
        data-autocomplete-light-language="en"
        id="id_test" name="test">
<option value="1">A</option>
</select>
        '''.strip()
        observed = six.text_type(form['test'].as_widget())

        self.assertHTMLEqual(observed, expected)

        form = Form(http.QueryDict('test=1'))
        expected = '''
<select data-autocomplete-light-function="select2"
        data-autocomplete-light-language="en"
        id="id_test" name="test">
<option value="1" %s>A</option>
</select>
        '''.strip() % selected_tag()
        observed = six.text_type(form['test'].as_widget())

        self.assertHTMLEqual(observed, expected)

    def test_widget_finds_correct_language(self):
        """Assert that a valid language code is found correctly."""
        self.assertEqual(select2_widget.get_i18n_name('en'), 'en')
        self.assertEqual(select2_widget.get_i18n_name('en-US'), 'en')
        self.assertEqual(select2_widget.get_i18n_name('fr-US'), 'fr')
        self.assertEqual(select2_widget.get_i18n_name('fr-FR'), 'fr')
        self.assertEqual(select2_widget.get_i18n_name('sr-Cyrl'), 'sr-Cyrl')
        self.assertEqual(select2_widget.get_i18n_name('zh-TW'), 'zh-TW')
        self.assertEqual(select2_widget.get_i18n_name('zh-Hant'), 'zh-TW')

    def test_widget_does_not_find_incorrect_language(self):
        """Assert that an invalid language code is not found."""
        self.assertEqual(select2_widget.get_i18n_name('ab'), None)
        self.assertEqual(select2_widget.get_i18n_name('cd'), None)
        self.assertEqual(select2_widget.get_i18n_name('ab-US'), None)


@override_settings(ROOT_URLCONF='tests.test_widgets')
class WidgetMixinTest(test.TestCase):  # noqa
    def test_widget_renders_without_attrs(self):
        """Assert that render will fallback to field name if no id."""
        class BaseWidget(object):
            def render(self, name, value, attrs=None):
                return ''

        class Widget(WidgetMixin, BaseWidget):
            def render_forward_conf(self, id):
                return six.text_type(id)

        widget = Widget(forward=['test'])

        # no attrs
        observed = widget.render('myname', '')
        self.assertEqual(observed, 'myname')

        # attrs without id
        observed = widget.render('myname', '', attrs={})
        self.assertEqual(observed, 'myname')

        # attrs with id
        observed = widget.render('myname', '', attrs={'id': 'myid'})
        self.assertEqual(observed, 'myid')
