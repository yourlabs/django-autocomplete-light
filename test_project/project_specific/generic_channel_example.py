import autocomplete_light

from models import Contact, Address

class MyGenericChannel(autocomplete_light.GenericChannelBase):
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

autocomplete_light.register(MyGenericChannel)
