from django.template import loader

from .base import AutocompleteBase


class AutocompleteTemplate(AutocompleteBase):
    """
    This extension of :py:class:`~.base.AutocompleteBase` supports two new
    attributes:

    .. py:attribute:: choice_template

        Name of the template to use to render a choice in the autocomplete. If
        none is specified, then :py:class:`~.base.AutocompleteBase` will render
        the choice.

    .. py:attribute:: autocomplete_template

        Name of the template to use to render the autocomplete. Again, fall
        back on :py:class:`~.base.AutocompleteBase` if this is None.
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
        Render :py:attr:`autocomplete_template` with base context and ``{{
        choices }}``. If :py:attr:`autocomplete_template` is None then fall
        back on :py:meth:`.base.AutocompleteBase.autocomplete_html`.
        """
        if self.autocomplete_template:
            choices = self.choices_for_request()

            return self.render_template_context(self.autocomplete_template,
                {'choices': choices})
        else:
            return super(AutocompleteTemplate, self).autocomplete_html()

    def choice_html(self, choice):
        """
        Render :py:attr:`choice_template` with base context and ``{{ choice
        }}``. If :py:attr:`choice_template` is None then fall back on
        :py:meth:`.base.AutocompleteBase.choice_html()`.
        """
        if self.choice_template:
            return self.render_template_context(self.choice_template,
                {'choice': choice})
        else:
            return super(AutocompleteTemplate, self).choice_html(choice)
