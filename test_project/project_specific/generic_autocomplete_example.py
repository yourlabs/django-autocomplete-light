import autocomplete_light

from models import Contact, Address

class MyGenericAutocomplete(autocomplete_light.AutocompleteGenericBase):
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

    def query_filter(self, results):
        q = self.request.GET.get('q', None)

        if q:
            if results.model == Address:
                results = results.filter(street__icontains=q)
            elif results.model == Contact:
                results = results.filter(name__icontains=q)

        return results

autocomplete_light.register(MyGenericChannel)
