"""Select2 widget implementation module."""

from dal.widgets import QuerySetSelectMixin

from django import forms


class Select2WidgetMixin(object):
    """Mixin for Select2 widgets."""

    class Media:
        """Automatically include static files for the admin."""

        css = {
            'all': (
                'autocomplete_light/vendor/select2/dist/css/select2.css',
                'autocomplete_light/select2.css',
            )
        }
        js = (
            'autocomplete_light/jquery.init.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/vendor/select2/dist/js/select2.full.js',
            'autocomplete_light/select2.js',
        )

    autocomplete_function = 'select2'


class ModelSelect2(QuerySetSelectMixin,
                   Select2WidgetMixin,
                   forms.Select):
    """Select widget for QuerySet choices and Select2."""


class ModelSelect2Multiple(QuerySetSelectMixin,
                           Select2WidgetMixin,
                           forms.SelectMultiple):
    """SelectMultiple widget for QuerySet choices and Select2."""


class TagSelect2(ModelSelect2Multiple):
    """ModelSelect2Multiple for tags."""

    def build_attrs(self, *args, **kwargs):
        """Automatically set data-tags=1."""
        attrs = super(TagSelect2, self).build_attrs(*args, **kwargs)
        attrs.setdefault('data-tags', 1)
        return attrs
