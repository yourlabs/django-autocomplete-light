from __future__ import unicode_literals

from django.utils.encoding import force_text

from .list import AutocompleteList

__all__ = ('AutocompleteChoiceList',)


class AutocompleteChoiceList(AutocompleteList):
    """
    Simple :py:class:`~.list.AutocompleteList` implementation which expects
    :py:attr:`choices` to be a list of tuple choices in the fashion of
    :py:attr:`django:django.db.models.Field.choices`.

    .. py:attribute:: choices

        List of choice tuples ``(value, label)`` like
        :py:attr:`django:django.db.models.Field.choices`. Example::

            choices = (
                ('v', 'Video'),
                ('p', 'Paper'),
            )

    .. py:attribute:: limit_choices

        The maximum of items to suggest from :py:attr:`choices`.

    .. py:attribute:: order_by

        :py:meth:`~.choice_list.AutocompleteChoiceList.order_choices` will use
        this against :py:attr:`choices` as an argument :py:func:`sorted`.
    """
    def order_by(cls, choice):
        return force_text(choice[1]).lower()

    def choices_for_values(self):
        """
        Return any :py:attr:`choices` that is in :py:attr:`values`.
        """
        values_choices = []

        for choice in self.choices:
            if choice[0] in self.values:
                values_choices.append(choice)

        return self.order_choices(values_choices)

    def choices_for_request(self):
        """
        Return any :py:attr:`choices` tuple that contains the search string. It
        is case insensitive and ignores spaces.
        """
        requests_choices = []
        q = self.request.GET.get('q', '').lower().strip()

        for choice in self.choices:
            m = force_text(choice[0]).lower() + force_text(choice[1]).lower()
            if q in m:
                requests_choices.append(choice)

        return self.order_choices(requests_choices)[0:self.limit_choices]

    def choice_value(self, choice):
        """ Return item 0 of the choice tuple. """
        return choice[0]

    def choice_label(self, choice):
        """ Return item 1 of the choice tuple. """
        return choice[1]
