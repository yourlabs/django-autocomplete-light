from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

__all__ = ('AutocompleteInterface', 'AutocompleteBase')


class AutocompleteInterface(object):
    """
    This is the minimum to implement in a custom Autocomplete class. It has two
    attributes:

    values
        A list of values which validate_values() and choices_for_values()
        should use.

    request
        A request object which choices_for_request() and autocomplete_html()
        should use.

    An autocomplete proposes "choices". A choice has a "value". When the user
    selects a "choice", then it is converted to a "value".
    """

    def __init__(self, request=None, values=None):
        """
        Class constructor sets the given request and values as instance
        attributes, casting values to list if necessary.
        """
        self.request = request

        if hasattr(values, '__iter__'):
            self.values = values
        else:
            self.values = [values]

    def autocomplete_html(self):
        """
        Return the HTML autocomplete that should be displayed under the text
        input. Use self.request if set.
        """
        raise NotImplemented()

    def validate_values(self):
        """
        Return True if self.values are all valid.
        """
        raise NotImplemented()

    def choices_for_values(self):
        """
        Return the list of choices corresponding to self.values.
        """
        raise NotImplemented()

    def get_absolute_url(self):
        """
        Return the absolute url for this autocomplete, using
        autocomplete_light_autocomplete url
        """
        return urlresolvers.reverse('autocomplete_light_autocomplete', args=(
            self.__class__.__name__,))


class AutocompleteBase(AutocompleteInterface):
    """
    A basic implementation of AutocompleteInterface that renders HTML and
    should fit most cases. However, it requires to overload
    choices_for_request().
    """
    choice_html_format = u'<div data-value="%s">%s</div>'
    empty_html_format = u'<div><em>%s</em></div>'
    autocomplete_html_format = u'%s'
    add_another_url_name = None

    def choices_for_request(self):
        """
        Return the list of choices that are available. Uses self.request if
        set. Use self.request if set, may be used by autocomplete_html().
        """
        raise NotImplemented()

    def validate_values(self):
        """
        Return True if all the values are available in choices_for_values().
        """
        return len(self.choices_for_values()) == len(self.values)

    def autocomplete_html(self):
        """
        Simple rendering of the autocomplete.
        """
        html = []

        for choice in self.choices_for_request():
            html.append(self.choice_html(choice))

        if not html:
            html = self.empty_html_format % _('no matches found').capitalize()

        return self.autocomplete_html_format % ''.join(html)

    def choice_html(self, choice):
        """
        Return a choice formated according to self.choice_html_format.
        """
        return self.choice_html_format % (
            self.choice_value(choice), self.choice_label(choice))

    def choice_value(self, choice):
        """
        Convert a choice to a value.
        """
        return unicode(choice)

    def choice_label(self, choice):
        """
        Convert a choice to a label.
        """
        return unicode(choice)
