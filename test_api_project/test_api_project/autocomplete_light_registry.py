import urllib

from django import http
from django.utils import simplejson

import autocomplete_light

from cities_light.contrib.autocomplete_light_channels import CityChannel
from cities_light.models import City, Country

class RemoteCountryChannel(autocomplete_light.JSONChannelBase):
    bootstrap = 'remotecountry'
    source_url = 'http://localhost:8000/cities_light/country/'

    def post(self, request, *args, **kwargs):
        result = simplejson.loads(request.POST['result'])
        return http.HttpResponse(self.fetch(result['source_url']).pk, 
            status=201)

    def model_for_source_url(self, url):
        if 'cities_light/city/' in url:
            return City
        elif 'cities_light/country/' in url:
            return Country

    def fetch(self, url):
        model_class = self.model_for_source_url(url)

        fh = urllib.urlopen(url)
        data = simplejson.loads(fh.read())
        data.pop('url')
        fh.close()

        for key, value in data.items():
            if isinstance(value, str) and settings.DATA_MASTER in value:
                data[key] = self.fetch(value)
        model, created = model_class.objects.get_or_create(**data)
        return model

    def get_source_url(self, limit):
        return '%s?%s' % (self.source_url, urllib.urlencode({'format': 'json',
            'name': self.request.GET.get('q', ''), 'limit': limit}))

    def get_extra_results(self, max):
        try:
            fh = urllib.urlopen(self.get_source_url(max))
            body = fh.read()
        except:
            return
        else:
            for data in simplejson.loads(body):
                url = data.pop('url')
                model = self.model(**data)
                model._source_url = url
                yield model

    def get_results(self, values=None):
        results = super(RemoteCountryChannel, self).get_results(values)

        if self.request:
            room = self.limit_results - len(results)

            if room > 0:
                results = list(results)
                results += [result for result in self.get_extra_results(room)]
        
        return results

    def result_as_dict(self, result):
        result_url = getattr(result, '_source_url', None)

        if result_url:
            return {'source_url': result_url}
        else:
            return {'value': result.pk}

autocomplete_light.register(Country, RemoteCountryChannel)
autocomplete_light.register(City, CityChannel)
