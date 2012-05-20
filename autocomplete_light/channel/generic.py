from django.contrib.contenttypes.models import ContentType

from autocomplete_light.generic import GenericForeignKeyField
from .base import ChannelBase

__all__ = ['GenericChannelBase']


class GenericChannelBase(ChannelBase):
    """
    Wraps around multiple querysets, from multiple model classes, rather than
    just one.

    This is also interresting as it overrides **all** the default model logic
    from ChannelBase. Hell, you could even copy it and make your
    CSVChannelBase, a channel that uses a CSV file as backend. But only if
    you're really bored or for a milion dollars.
    """

    def result_as_value(self, result):
        """
        Rely on GenericForeignKeyField to return a string containing the
        content type id and object id of the result.

        Because this channel is made for that field, and to avoid code
        duplication.
        """
        field = GenericForeignKeyField()
        return field.prepare_value(result)

    def order_results(self, results):
        """
        Return results, **without** doing any ordering.

        In most cases, you would not have to override this method as querysets
        should be ordered by default, based on model.Meta.ordering.
        """
        return results  # can't order because don't know what model type

    def get_results(self, values=None):
        """
        Return results for each queryset returned by get_querysets().

        Note that it limits each queryset's to self.limit_result. If you want a
        maximum of 12 suggestions and have a total of 4 querysets, then
        self.limit_results should be set to 3.
        """
        for model, queryset in self.get_querysets().items():
            if values is not None:
                queryset = self.values_filter(queryset, values)

            elif self.request:
                queryset = self.query_filter(queryset)

            for result in self.order_results(queryset)[0:self.limit_results]:
                yield result

    def are_valid(self, values):
        """
        Return True if it can find all the models refered by values.
        """
        for value in values:
            # some nice Q action could be done here
            content_type_id, object_id = value.split('-')
            model = ContentType.objects.get_for_id(
                content_type_id).model_class()

            if not model.objects.filter(pk=object_id).count():
                return False

        return True

    def values_filter(self, results, values):
        """
        Filter out any result from results that is not refered to by values.
        """
        ctype = ContentType.objects.get_for_model(results.model).pk
        ids = [x.split('-')[1] for x in values \
            if int(x.split('-')[0]) == ctype]
        return results.filter(pk__in=ids)
