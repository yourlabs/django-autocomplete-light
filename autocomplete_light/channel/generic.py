from django.contrib.contenttypes.models import ContentType

from .base import ChannelBase

__all__ = ['GenericChannelBase',]

class GenericChannelBase(ChannelBase):

    def result_as_value(self, result):
        """
        Rely on GenericForeignKeyField to return a string containing the
        content type id and object id of the result.

        Because this channel is made for that field, and to avoid code
        duplication.
        """
        return GenericForeignKeyField.prepare_value(None, result)

    def order_results(self):
        return results # can't order

    def get_results(self, values=None):
        for model, queryset in self.get_querysets().items():
            if values is not None:
                queryset = self.values_filter(queryset, values)
            
            elif self.request:
                queryset = self.query_filter(queryset)
            
            for result in self.order_results(queryset)[0:self.limit_results]:
                yield result

    def are_valid(self, values):
        for value in values:
            # some nice Q action could be done here
            content_type_id, object_id = value.split('-')
            model = ContentType.objects.get_for_id(content_type_id).model_class()
            if not model.objects.filter(pk=object_id).count():
                return False

        return True

    def values_filter(self, results, values):
        ctype = ContentType.objects.get_for_model(results.model).pk
        ids = [x.split('-')[1] for x in values if int(x.split('-')[0]) == ctype]
        return results.filter(pk__in=ids)
