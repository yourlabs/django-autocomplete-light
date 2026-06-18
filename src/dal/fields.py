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
                result.append(tuple(choice))
            else:
                result.append((choice, choice))
        return result


class ListChoiceField(ChoiceField):
    """ChoiceField whose valid choices come from a list or callable."""

    def __init__(self, choice_list=None, *args, **kwargs):
        kwargs['choices'] = ChoiceCallable(choice_list)
        super().__init__(*args, **kwargs)


class ListCreateChoiceField(ListChoiceField):
    """Like ListChoiceField but allows values created on-the-fly."""

    def validate(self, value):
        super(ChoiceField, self).validate(value)
