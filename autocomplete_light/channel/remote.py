import urllib

from django import http
from django.utils import simplejson

from json import JSONChannelBase

__all__ = ['RemoteChannelBase', ]


class RemoteChannelBase(JSONChannelBase):
    """
    Uses an API to propose suggestions from an HTTP API, tested with
    djangorestframework.

    model_for_source_url
        A **very important function to override!** take an API URL and return
        the corresponding model class. This is API specific, there is a
        complete example in cities_light.contrib.

    source_url
        The full URL to the list API. For example, to a djangorestframework
        list view.

    An example implementation usage is demonstrated in the django-cities-light
    contrib folder.

    Autocomplete box display chronology:

    - autocomplete.js requests autocomplete box to display for an input,
    - get_results() fetches some extra results via get_remote_results(),
    - get_remote_results() calls source_url and returns a list of models,
    - the remote results are rendered after the local results in widget.html.
      It includes some JSON in a hidden textarea, like the API's url for each
      result.
    
    Remote result selection chronology:

    - deck.js calls remoteGetValue() instead of the default getValue(),
    - remoteGetValue() posts the json from the result to ChannelView,
    - ChannelView.post() does its job of proxying RemoteChannelBase.post(),
    - RemoteChannelBase.post() returns an http response which body is just the
      pk of the result in the local database, using self.fetch_result(),
    - self.fetch_result() passes the API url of the result and recursively
      saves the remote models into the local database, returning the id of the
      newly created object.
    """

    bootstrap = 'remote'
    static_list = ('autocomplete_light/remote.js', )

    def post(self, request, *args, **kwargs):
        """
        Take POST variable 'result', install it in the local database, return
        the newly created id.

        The HTTP response has status code 201 Created.
        """
        result = simplejson.loads(request.POST['result'])
        pk = self.fetch_result(result)
        return http.HttpResponse(pk, status=201)

    def model_for_source_url(self, url):
        """
        Take an URL from the API this remote channel is supposed to work with,
        return the model class to use for that url.

        It is only needed for the default implementation of fetch(), because it
        has to follow relations recursively.
        """
        raise NotImplemented()

    def fetch_result(self, result):
        """
        Take a result's dict representation, return it's local pk which might
        have been just created.

        If your channel works with 0 to 1 API call, consider overriding this
        method.
        If your channel is susceptible of using several different API calls,
        consider overriding fetch().
        """
        return self.fetch(result['source_url']).pk

    def fetch(self, url):
        """
        Given an url to a remote object, return the corresponding model from
        the local database.

        The default implementation expects url to respond with a JSON dict of
        the attributes of an object.

        For relation attributes, it expect the value to be another url that
        will respond with a JSON dict of the attributes of the related object.

        It calls model_for_source_url() to find which model class corresponds
        to which url. This allows fetch() to be recursive.
        """
        model_class = self.model_for_source_url(url)

        fh = urllib.urlopen(url)
        data = simplejson.loads(fh.read())
        data.pop('url')
        fh.close()

        for key, value in data.items():
            field = model_class._meta.get_field_by_name(key)[0]
            if getattr(field, 'rel', None) and isinstance(value, (unicode, str)):
                data[key] = self.fetch(value)
        model, created = model_class.objects.get_or_create(**data)
        return model

    def get_results(self, values=None):
        """
        Returns a list of results from both the local database and the API if
        in the context of a request.

        Using self.limit_results and the number of local results, adds results
        from get_remote_results().
        """
        results = super(RemoteChannelBase, self).get_results(values)
        unicodes = [unicode(result) for result in results]

        if self.request:
            room = self.limit_results - len(results)

            if room > 0:
                results = list(results)
                
                for result in self.get_remote_results(room):
                    # avoid data that's already in local
                    if unicode(result) in unicodes:
                        continue
                
                    results.append(result)
        
        return results

    def get_remote_results(self, max):
        """
        Parses JSON from the API, return model instances.

        The JSON should contain a list of dicts. Each dict should contain the
        attributes of an object. Relation attributes should be represented by
        their url in the API, which is set to model._source_url.
        """
        url = self.get_source_url(max)

        try:
            fh = urllib.urlopen(url)
            body = fh.read()
        except:
            return
        else:
            for data in simplejson.loads(body):
                url = data.pop('url')

                for name in data.keys():
                    field = self.model._meta.get_field_by_name(name)[0]
                    if getattr(field, 'rel', None):
                        data.pop(name)
                model = self.model(**data)
                model._source_url = url
                yield model


    def result_as_dict(self, result):
        """
        Return the result pk or _source_url.
        """
        result_url = getattr(result, '_source_url', None)

        if result_url:
            return {'source_url': result_url}
        else:
            return {'value': result.pk}

    def get_source_url(self, limit):
        """
        Return an API url for the current autocomplete request.

        By default, return self.source_url with the data dict returned by
        get_source_url_data().
        """
        return '%s?%s' % (self.source_url, urllib.urlencode(
            self.get_source_url_data(limit)))


    def get_source_url_data(self, limit):
        """
        Given a limit of items, return a dict of data to send to the API.

        By default, it passes current request GET arguments, along with format:
        'json' and the limit.
        """
        data = {}
        if self.request:
            for key, value in self.request.GET.items():
                data[key] = value

        data.update({
            'format': 'json',
            'limit': limit,
        })

        return data
