"""Select2 widget implementation module."""

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
from django.utils import six
from django.utils import translation


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
            lang_code = translation.to_locale(lang_code).replace('_', '-')
        return lang_code

    @property
    def media(self):
        """Return JS/CSS resources for the widget."""
        extra = '' if settings.DEBUG else '.min'
        i18n_name = SELECT2_TRANSLATIONS.get(translation.get_language())
        i18n_file = (
            'admin/js/vendor/select2/i18n/%s.js' % i18n_name,
        ) if i18n_name else ()

        return forms.Media(
            js=(
                'admin/js/vendor/jquery/jquery%s.js' % extra,
                'autocomplete_light/jquery.init.js',
                'admin/js/vendor/select2/select2.full%s.js' % extra,
            ) + i18n_file + (
                'autocomplete_light/autocomplete.init.js',
                'autocomplete_light/forward.js',
                'autocomplete_light/select2.js',
                'autocomplete_light/jquery.post-setup.js',
            ),
            css={
                'screen': (
                    'admin/css/vendor/select2/select2%s.css' % extra,
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

            if isinstance(v, six.string_types):
                for t in v.split(','):
                    values.add(self.option_value(t))
            else:
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
