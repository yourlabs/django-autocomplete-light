"""Widgets for Select2 and django-taggit."""

from dal_select2.widgets import TagSelect2

from django import VERSION
from django.utils import six


class TaggitSelect2(TagSelect2):
    """Select2 tag widget for taggit's TagField."""

    """
    if we want to edit an instance and fill tags with already added tags it causes exceptio:
    Tag Object Not Iterable
    
    so i overwrited format_value , options in TaggitSelect2 and now it's good to go
    """
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
                values.add(self.option_value(v))
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
            yield self.option_value(real_values)

    def build_attrs(self, *args, **kwargs):
        """Add data-tags=","."""
        attrs = super(TaggitSelect2, self).build_attrs(*args, **kwargs)
        attrs['data-tags'] = ','
        return attrs

    def value_from_datadict(self, data, files, name):
        """Handle multi-word tag.

        Insure there's a comma when there's only a single multi-word tag,
        or tag "Multi word" would end up as "Multi" and "word".
        """
        value = super(TaggitSelect2, self).value_from_datadict(data,
                                                               files, name)
        if value and ',' not in value:
            value = '%s,' % value
        return value

    def option_value(self, value):
        """Return tag.name attribute of value."""
        return value.tag.name if hasattr(value, 'tag') else value

    def render_options(self, *args):
        """
        Render only selected tags.

        Remove when Django < 1.10 support is dropped.
        """
        selected_choices_arg = 1 if VERSION < (1, 10) else 0
        selected_choices = args[selected_choices_arg]

        # When the data hasn't validated, we get the raw input here
        if isinstance(selected_choices, six.text_type):
            choices = [c.strip() for c in selected_choices.split(',')]
        else:
            # Filter out None values, not needed for autocomplete
            choices = [c.tag.name for c in selected_choices if c]

        options = [
            '<option value="%s" selected="selected">%s</option>' % (
                c, c) for c in choices
        ]

        return '\n'.join(options)
