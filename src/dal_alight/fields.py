"""Form fields for dal_alight — mirrors dal_select2.fields without select2."""

from django.forms import ChoiceField


class ChoiceCallable:
    """Choices wrapper that supports callable choices."""

    def __init__(self, choices):
        self.choices = choices

    def __call__(self):
        result = []
        choices = self.choices() if callable(self.choices) else self.choices
        for choice in choices or []:
            if isinstance(choice, (list, tuple)):
                result.append(choice)
            else:
                result.append((choice, choice))
        return result


class AlightListChoiceField(ChoiceField):
    """ChoiceField whose valid choices come from a list or callable.

    Useful when ``AlightListView`` serves the autocomplete and the stored
    value is the text itself (no PK).
    """

    def __init__(self, choice_list=None, required=True, widget=None,
                 label=None, initial=None, help_text='', *args, **kwargs):
        choices = ChoiceCallable(choice_list)
        super().__init__(
            choices=choices, required=required, widget=widget, label=label,
            initial=initial, help_text=help_text, *args, **kwargs,
        )


class AlightListCreateChoiceField(AlightListChoiceField):
    """Like ``AlightListChoiceField`` but skips choice validation.

    Allows values created on-the-fly (via POST) to be accepted by the form.
    """

    def validate(self, value):
        # Only check for empty; do not validate against the choice list.
        super(ChoiceField, self).validate(value)
