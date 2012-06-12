import types

from django.template import loader

from .base import AutocompleteBase


class AutocompleteTemplate(AutocompleteBase):
    choice_template = None
    autocomplete_template = None

    def get_base_context(self):
        return {
            'request': self.request,
            'autocomplete': self,
        }

    def render_template_context(self, template, extra_context=None):
        context = self.get_base_context()
        context.update(extra_context or {})
        return loader.render_to_string(template, context)

    def autocomplete_html(self):
        if self.autocomplete_template:
            choices = self.choices_for_request()

            return self.render_template_context(self.autocomplete_template,
                {'choices': choices})
        else:
            return super(AutocompleteTemplate, self).autocomplete_html()

    def choice_html(self, choice):
        if self.choice_template:
            return self.render_template_context(self.choice_template,
                {'choice': choice})
        else:
            return super(AutocompleteTemplate, self).choice_html(choice)
