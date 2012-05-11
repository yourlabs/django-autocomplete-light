"""
The channel.base module provides a channel class which you can extend to make
your own channel. It also serves as default channel class.
"""

from django.core import urlresolvers
from django.template import loader
from django.utils.translation import ugettext_lazy as _

__all__ = ('ChannelBase',)


class ChannelBase(object):
    """
    A basic implementation of a channel, which should fit most use cases.

    Attributes:

    model
        The model class this channel serves. If None, a new class will be
        created in registry.register, and the model attribute will be set in
        that subclass. So you probably don't need to worry about it, just know
        that it's there for you to use.

    result_template
        The template to use in result_as_html method, to render a single
        autocomplete suggestion. By default, it is
        autocomplete_light/channelname/result.html or
        autocomplete_light/result.html.

    autocomplete_template
        The template to use in render_autocomplete method, to render the
        autocomplete box. By default, it is
        autocomplete_light/channelname/autocomplete.html or
        autocomplete_light/autocomplete.html.

    search_field
        The name of the field that the default implementation of query_filter
        uses. Default is 'name'.

    limit_results
        The number of results that this channel should return. For example, if
        query_filter returns 50 results and that limit_results is 20, then the
        first 20 of 50 results will be rendered. Default is 20.

    bootstrap
        The name of the bootstrap kind. By default, deck.js will only
        initialize decks for wrappers that have data-bootstrap="normal". If
        you want to implement your own bootstrapping logic in javascript,
        then you set bootstrap to anything that is not "normal". Default is
        'normal'.

    placeholder
        The initial text in the autocomplete text input.
    """

    model = None
    search_field = 'name'
    limit_results = 20
    bootstrap = 'normal'
    placeholder = _(u'type some text to search in this autocomplete')
    result_template = None
    autocomplete_template = None

    def __init__(self):
        """
        Set result_template and autocomplete_template if necessary.
        """
        if not self.result_template:
            self.result_template = [
                'autocomplete_light/%s/result.html' % self.__class__.__name__.lower(),
                'autocomplete_light/result.html',
            ]

        if not self.autocomplete_template:
            self.autocomplete_template = [
                'autocomplete_light/%s/autocomplete.html' % self.__class__.__name__.lower(),
                'autocomplete_light/autocomplete.html',
            ]

    def get_absolute_url(self):
        """
        Return the absolute url for this channel, using
        autocomplete_light_channel url
        """
        return urlresolvers.reverse('autocomplete_light_channel', args=(
            self.__class__.__name__,))

    def as_dict(self):
        """
        Return a dict of variables for this channel, it is used by javascript.
        """
        return {
            'url': self.get_absolute_url(),
            'name': self.__class__.__name__
        }

    def init_for_request(self, request, *args, **kwargs):
        """
        Set self.request, self.args and self.kwargs, useful in query_filter.
        """
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def query_filter(self, results):
        """
        Filter results using the request.

        By default this will expect results to be a queryset, and will filter
        it with self.search_field + '__icontains'=self.request['q'].
        """
        q = self.request.GET.get('q', None)

        if q:
            kwargs = {"%s__icontains" % self.search_field: q}
            results = results.filter(**kwargs)

        return results

    def values_filter(self, results, values):
        """
        Filter results based on a list of values.

        By default this will expect values to be an iterable of model ids, and
        results to be a queryset. Thus, it will return a queryset where pks are
        in values.
        """
        results = results.filter(pk__in=values)
        return results

    def get_queryset(self):
        """
        Return a queryset for the channel model.
        """
        return self.model.objects.all()

    def get_results(self, values=None):
        """
        Return an iterable of result to display in the autocomplete box.

        By default, it will:

        - call self.get_queryset(),
        - call values_filter() if values is not None,
        - call query_filter() if self.request is set,
        - call order_results(),
        - return a slice from offset 0 to self.limit_results.
        """
        results = self.get_queryset()

        if values is not None:
            # used by the widget to prerender existing values
            results = self.values_filter(results, values)

        elif self.request:
            # used by the autocomplete
            results = self.query_filter(results)

        return self.order_results(results)[0:self.limit_results]

    def order_results(self, results):
        """
        Return the result list after ordering.

        By default, it expects results to be a queryset and order it by
        search_field.
        """
        return results.order_by(self.search_field).distinct()

    def are_valid(self, values):
        """
        Return True if the values are valid.

        By default, expect values to be a list of object ids, return True if
        all the ids are found in the queryset.
        """
        return self.get_queryset().filter(pk__in=values).count() == len(values)

    def result_as_html(self, result):
        """
        Return the html representation of a result for display in the deck
        and autocomplete box.

        By default, render result_template with channel and result in the
        context.
        """
        return loader.render_to_string(self.result_template, {
            'channel': self,
            'result': result,
        })

    def render_autocomplete(self):
        """
        Render the autocomplete suggestion box.

        By default, render self.autocomplete_template with the channel in the
        context.
        """
        return loader.render_to_string(self.autocomplete_template, {
            'channel': self,
        })
