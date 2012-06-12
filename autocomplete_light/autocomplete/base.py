from django.core import urlresolvers


class AutocompleteInterface(object):
    def __init__(self, request=None, values=None):
        self.request = request
        self.values = values

    def autocomplete_html(self):
        raise NotImplemented()

    def validate_values(self):
        raise NotImplemented()

    def choices_for_request(self):
        raise NotImplemented()

    def choices_for_values(self):
        raise NotImplemented()

    def get_absolute_url(self):
        """
        Return the absolute url for this autocomplete, using
        autocomplete_light_autocomplete url
        """
        return urlresolvers.reverse('autocomplete_light_autocomplete', args=(
            self.__class__.__name__,))


class AutocompleteBase(AutocompleteInterface):
    choice_html_format = u'<div data-value="%s">%s</div>'
    autocomplete_html_format = u'%s'

    def validate_values(self):
        return len(self.choices_for_values()) == len(self.values)

    def autocomplete_html(self):
        html = []

        for choice in self.choices_for_request():
            html.append(self.choice_html(choice))

        return self.autocomplete_html_format % ''.join(html)

    def choice_html(self, choice):
        return self.choice_html_format % (
            self.choice_value(choice), self.choice_label(choice))

    def choice_value(self, choice):
        return unicode(choice)

    def choice_label(self, choice):
        return unicode(choice)
