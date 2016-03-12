"""Widgets for Select2 and django-taggit."""

from dal_select2.widgets import TagSelect2

from django import VERSION
from django.utils import six


class TaggitSelect2(TagSelect2):
    """Select2 tag widget for taggit's TagField."""

    def render_options(self, *args):
        """Render only selected tags."""
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
