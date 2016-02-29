"""Widgets for Select2 and django-taggit."""

from dal_select2.widgets import TagSelect2

from django import VERSION


class TaggingSelect2(TagSelect2):
    """Select2 tag widget for tagging's TagField."""

    def render_options(self, *args):
        """Render only selected tags."""
        selected_choices_arg = 1 if VERSION < (1, 10) else 0

        selected_choices = args[selected_choices_arg]

        if selected_choices:
            # Here, selected_choices is a string of comma-separated tags:
            # that's how the tagging field works, otherwise it'd be an empty
            # list because that's how the select field uses for None values
            selected_choices = selected_choices.split(',')

        options = [
            '<option value="%s" selected="selected">%s</option>' % (c, c)
            for c in selected_choices
        ]

        return '\n'.join(options)
