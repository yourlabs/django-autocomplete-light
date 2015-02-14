from __future__ import unicode_literals

from django.utils.encoding import force_text

__all__ = ('AutocompleteList',)


class AutocompleteList(object):
    """
    Simple Autocomplete implementation which expects :py:attr:`choices` to be a
    list of string choices.

    .. py:attribute:: choices

        List of string choices.

    .. py:attribute:: limit_choices

        The maximum of items to suggest from :py:attr:`choices`.

    .. py:attribute:: order_by

        :py:meth:`~.list.AutocompleteList.order_choices` will use this against
        :py:attr:`choices` as an argument :py:func:`sorted`.

    It was mainly used as a starter for me when doing test-driven development
    and to ensure that the Autocomplete pattern would be concretely simple and
    yet powerful.
    """

    limit_choices = 20

    def order_by(cls, choice):
        return force_text(choice).lower()

    def choices_for_values(self):
        """
        Return any :py:attr:`choices` that is in :py:attr:`values`.
        """
        values_choices = []

        for choice in self.choices:
            if choice in self.values:
                values_choices.append(choice)

        return self.order_choices(values_choices)

    def choices_for_request(self):
        """
        Return any :py:attr:`choices` that contains the search string. It is
        case insensitive and ignores spaces.
        """
        assert self.choices is not None, 'autocomplete.choices is not set'

        requests_choices = []
        q = self.request.GET.get('q', '').lower().strip()

        for choice in self.choices:
            if q in force_text(choice).lower():
                requests_choices.append(choice)

        return self.order_choices(requests_choices)[0:self.limit_choices]

    def order_choices(self, choices):
        """
        Run :py:func:`sorted` against ``choices`` and :py:attr:`order_by`.
        """
        return sorted(choices, key=self.order_by)
