"""Widgets for Select2 and django-taggit."""

from dal_select2.widgets import TagSelect2

from django import VERSION


class TaggitSelect2(TagSelect2):
    """Select2 tag widget for taggit's TagField."""

    def render_options(self, *args):
        """Render only selected tags."""
        selected_choices_arg = 1 if VERSION < (1, 10) else 0

        # Filter out None values, not needed for autocomplete
        selected_choices = [c for c in args[selected_choices_arg] if c]

        options = [
            '<option value="%s" selected="selected">%s</option>' % (
                c.tag.name, c.tag.name) for c in selected_choices
        ]

        return '\n'.join(options)
