"""Select2 widget implementation module."""

try:
    from functools import lru_cache
except:
    lru_cache = None

from dal.widgets import (
    QuerySetSelectMixin,
    Select,
    SelectMultiple,
    WidgetMixin
)

from django import forms
from django.conf import settings
try:
    # SELECT2_TRANSLATIONS is Django 2.x only
    from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
except ImportError:
    SELECT2_TRANSLATIONS = {}
from django.contrib.staticfiles import finders
from django.utils import translation
from django.utils.itercompat import is_iterable

import six


I18N_PATH = 'vendor/select2/dist/js/i18n/'


def get_i18n_name(lang_code):
    """Ensure lang_code is supported by Select2."""
    lower_lang = lang_code.lower()
    split_lang = lang_code.split('-')[0]
    # Use the SELECT2_TRANSLATIONS if available
    if SELECT2_TRANSLATIONS:
        if lower_lang in SELECT2_TRANSLATIONS:
            return SELECT2_TRANSLATIONS.get(lower_lang)
        elif split_lang in SELECT2_TRANSLATIONS:
            return SELECT2_TRANSLATIONS.get(split_lang)
    # Otherwise fallback to manually checking if the static file exists
    if finders.find('%s%s.js' % (I18N_PATH, lang_code)):
        return lang_code
    elif finders.find('%s%s.js' % (I18N_PATH, split_lang)):
        return lang_code.split('-')[0]


if lru_cache:
    get_i18n_name = lru_cache()(get_i18n_name)
else:
    import warnings
    warnings.warn('Python2: no cache on get_i18n_name until contribution')


class Select2WidgetMixin(object):
    """Mixin for Select2 widgets."""

    def build_attrs(self, *args, **kwargs):
        """Set data-autocomplete-light-language."""
        attrs = super(Select2WidgetMixin, self).build_attrs(*args, **kwargs)
        lang_code = self._get_language_code()
        if lang_code:
            attrs.setdefault('data-autocomplete-light-language', lang_code)
        return attrs

    def _get_language_code(self):
        """Return language code or None."""
        lang_code = translation.get_language()
        if lang_code:
            lang_code = get_i18n_name(
                translation.to_locale(lang_code).replace('_', '-')
            )
        return lang_code

    @property
    def media(self):
        """Return JS/CSS resources for the widget."""
        extra = '' if settings.DEBUG else '.min'
        i18n_name = self._get_language_code()
        i18n_file = (
            '%s%s.js' % (I18N_PATH, i18n_name),
        ) if i18n_name else ()

        return forms.Media(
            js=(
                'autocomplete_light/jquery.init.js',
                'vendor/select2/dist/js/select2.full%s.js' % extra,
            ) + i18n_file + (
                'autocomplete_light/autocomplete.init.js',
                'autocomplete_light/forward.js',
                'autocomplete_light/select2.js',
                'autocomplete_light/jquery.post-setup.js',
            ),
            css={
                'screen': (
                    'vendor/select2/dist/css/select2%s.css' % extra,
                    'admin/css/autocomplete.css',
                    'autocomplete_light/select2.css',
                ),
            },
        )

    autocomplete_function = 'select2'


class Select2(Select2WidgetMixin, Select):
    """Select2 widget for regular choices."""


class Select2Multiple(Select2WidgetMixin, SelectMultiple):
    """Select2Multiple widget for regular choices."""


class ListSelect2(WidgetMixin, Select2WidgetMixin, forms.Select):
    """Select widget for regular choices and Select2."""


class ModelSelect2(QuerySetSelectMixin,
                   Select2WidgetMixin,
                   forms.Select):
    """Select widget for QuerySet choices and Select2."""


class ModelSelect2Multiple(QuerySetSelectMixin,
                           Select2WidgetMixin,
                           forms.SelectMultiple):
    """SelectMultiple widget for QuerySet choices and Select2."""


class TagSelect2(WidgetMixin,
                 Select2WidgetMixin,
                 forms.SelectMultiple):
    """Select2 in tag mode."""

    def build_attrs(self, *args, **kwargs):
        """Automatically set data-tags=1."""
        attrs = super(TagSelect2, self).build_attrs(*args, **kwargs)
        attrs.setdefault('data-tags', 1)
        return attrs

    def value_from_datadict(self, data, files, name):
        """Return a comma-separated list of options.

        This is needed because Select2 uses a multiple select even in tag mode,
        and the model field expects a comma-separated list of tags.
        """
        values = super(TagSelect2, self).value_from_datadict(data, files, name)
        return six.text_type(',').join(values)

    def option_value(self, value):
        """Return the HTML option value attribute for a value."""
        return value

    def format_value(self, value):
        """Return the list of HTML option values for a form field value."""
        if not isinstance(value, (tuple, list)):
            value = [value]

        values = set()
        for v in value:
            if not v:
                continue

            v = v.split(',') if isinstance(v, six.string_types) else v
            v = [v] if not is_iterable(v) else v
            for t in v:
                values.add(self.option_value(t))
        return values

    def options(self, name, value, attrs=None):
        """Return only select options."""
        # When the data hasn't validated, we get the raw input
        if isinstance(value, six.text_type):
            value = value.split(',')

        for v in value:
            if not v:
                continue

            real_values = v.split(',') if hasattr(v, 'split') else v
            real_values = [real_values] if not is_iterable(real_values) else real_values
            for rv in real_values:
                yield self.option_value(rv)

    def optgroups(self, name, value, attrs=None):
        """Return a list of one optgroup and selected values."""
        default = (None, [], 0)
        groups = [default]

        for i, v in enumerate(self.options(name, value, attrs)):
            default[1].append(
                self.create_option(v, v, v, True, i)
            )
        return groups
