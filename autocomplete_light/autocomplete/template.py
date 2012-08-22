import types

from django.template import loader

from .base import AutocompleteBase


class AutocompleteTemplate(AutocompleteBase):
    """
    This replacement for AutocompleteBase supports two new attributes:

    choice_template
        Name of the template to use to render a choice in the autocomplete. If
        none is specified, then ``AutocompleteBase`` will render the choice.

    autocomplete_template
        Name of the template to use to render the autocomplete. Again, fall
        back on ``AutocompleteBase`` if this is None.
    """
    choice_template = None
    autocomplete_template = None

    def get_base_context(self):
        """
        Return a dict to use as base context for all templates.

        It contains:

        - ``{{ request }}`` if available,
        - ``{{ autocomplete }}`` the "self" instance.
        """
        return {
            'request': self.request,
            'autocomplete': self,
        }

    def render_template_context(self, template, extra_context=None):
        """
        Render ``template`` with base context and ``extra_context``.
        """
        context = self.get_base_context()
        context.update(extra_context or {})
        return loader.render_to_string(template, context)

    def autocomplete_html(self):
        """
        Render ``autocomplete_template`` with base context and ``{{ choices
        }}``. If ``autocomplete_template`` is none then fall back on
        ``AutocompleteBase``.
        """
        if self.autocomplete_template:
            choices = self.choices_for_request()

            return self.render_template_context(self.autocomplete_template,
                {'choices': choices})
        else:
            return super(AutocompleteTemplate, self).autocomplete_html()

    def choice_html(self, choice):
        """
        Render choice_template with base context and ``{{ choice }}``. If
        ``choice_template`` is none then fall back on ``AutocompleteBase``.
        """
        if self.choice_template:
            return self.render_template_context(self.choice_template,
                {'choice': choice})
        else:
            return super(AutocompleteTemplate, self).choice_html(choice)
