from django.contrib.contenttypes.models import ContentType

import autocomplete_light

from models import Contact, Address

autocomplete_light.register(Contact)

class GenericChannel(autocomplete_light.JSONChannelBase):
    static_list = ('autocomplete_light/generic.js', )

    def result_as_dict(self, result):
        return {
            'content_type': ContentType.objects.get_for_model(result).pk,
            'object_id': result.pk,
        }

    def get_querysets(self):
        return {
            Contact: Contact.objects.all(),
            Address: Address.objects.all(),
        }

    def order_results(self, results):
        if results.model == Address:
            return results.order_by('street')
        elif results.model == Contact:
            return results.order_by('name')

    def get_results(self, values=None):
        for model, queryset in self.get_querysets().items():
            if values is not None:
                queryset = self.values_filter(queryset, values)
            
            elif self.request:
                queryset = self.query_filter(queryset)
            
            for result in self.order_results(queryset)[0:self.limit_results]:
                yield result

# manual registration for now
autocomplete_light.static_list += GenericChannel.static_list
autocomplete_light.registry['GenericChannel'] = GenericChannel
