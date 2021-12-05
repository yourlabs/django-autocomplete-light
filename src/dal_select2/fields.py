"""Select2 field implementation module."""

from django.forms import ChoiceField


class ChoiceCallable:
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


class Select2ListChoiceField(ChoiceField):
    """Allows a list of values to be used with a ChoiceField.

    Avoids unusual things that can happen if Select2ListView is used for
    a form where the text and value for choices are not the same.
    """

    def __init__(self, choice_list=None, required=True, widget=None,
                 label=None, initial=None, help_text='', *args, **kwargs):
        """Use a list to generate choices in a ChoiceField.

        .. py:param choice_list: The list to use to generate choices or a
        function that returns a list.
        """
        choices = ChoiceCallable(choice_list)

        super(Select2ListChoiceField, self).__init__(
            choices=choices, required=required, widget=widget, label=label,
            initial=initial, help_text=help_text, *args, **kwargs
        )


class Select2ListCreateChoiceField(Select2ListChoiceField):
    """Skips validation of choices so any value can be used."""

    def validate(self, value):
        """Do not validate choices but check for empty."""
        super(ChoiceField, self).validate(value)
