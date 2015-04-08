import autocomplete_light.shortcuts as autocomplete_light
from cities_light.models import Country, Region

autocomplete_light.register(Country, search_fields=('name', 'name_ascii',),
    autocomplete_js_attributes={'placeholder': 'country name ..'})


class AutocompleteRegion(autocomplete_light.AutocompleteModelBase):
    autocomplete_js_attributes={'placeholder': 'region name ..'}

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        country_id = self.request.GET.get('country_id', None)

        choices = self.choices.all()
        if q:
            choices = choices.filter(name_ascii__icontains=q)
        if country_id:
            choices = choices.filter(country_id=country_id)

        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Region, AutocompleteRegion)
