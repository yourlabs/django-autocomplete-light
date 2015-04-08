import urllib
import six

from django import http
from django.utils.encoding import force_text

from .model import AutocompleteModel

try:
    import json
except ImportError:
    from django.utils import simplejson as json


class AutocompleteRestModel(AutocompleteModel):
    widget_js_attributes = {'bootstrap': 'rest_model'}

    @property
    def model(self):
        return self.choices.model

    def post(self, request, *args, **kwargs):
        value = request.POST['value']
        pk = self.download_choice(value)
        return http.HttpResponse(pk, status=201)

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

    def model_for_source_url(self, url):
        """
        Take an URL from the API this remote channel is supposed to work with,
        return the model class to use for that url.

        It is only needed for the default implementation of download(), because
        it has to follow relations recursively.

        By default, it will return the model of self.choices.
        """
        return self.choices.model

    def choices_for_request(self):
        choices = super(AutocompleteRestModel, self).choices_for_request()
        unicodes = [force_text(choice) for choice in choices]

        slots = self.limit_choices - len(choices)

        if slots > 0:
            choices = list(choices)

            for choice in self.get_remote_choices(slots):
                # avoid data that's already in local
                if force_text(choice) in unicodes:
                    continue

                choices.append(choice)

        return choices

    def get_remote_choices(self, max):
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
            for data in json.loads(body):
                url = data.pop('url')

                for name in data.keys():
                    field = self.model._meta.get_field_by_name(name)[0]
                    if getattr(field, 'rel', None):
                        data.pop(name)
                model = self.model(**data)
                model.pk = url
                yield model

    def download_choice(self, choice):
        """
        Take a choice's dict representation, return it's local pk which might
        have been just created.

        If your channel works with 0 to 1 API call, consider overriding this
        method.
        If your channel is susceptible of using several different API calls,
        consider overriding download().
        """
        return self.download(choice).pk

    def download(self, url):
        """
        Given an url to a remote object, return the corresponding model from
        the local database.

        The default implementation expects url to respond with a JSON dict of
        the attributes of an object.

        For relation attributes, it expect the value to be another url that
        will respond with a JSON dict of the attributes of the related object.

        It calls model_for_source_url() to find which model class corresponds
        to which url. This allows download() to be recursive.
        """
        model_class = self.model_for_source_url(url)

        fh = urllib.urlopen(url)
        data = json.loads(fh.read())
        data.pop('url')
        fh.close()

        uniques = [f.name for f in model_class._meta.fields if f.unique]
        unique_data = {}

        for key, value in data.items():
            if key not in uniques:
                continue

            field = model_class._meta.get_field_by_name(key)[0]
            if getattr(field, 'rel', False):
                continue

            unique_data[key] = value

        if not unique_data:
            assert self.get_or_create_by, 'get_or_create_by needed'

            for key in self.get_or_create_by:
                if key in data.keys() and data[key]:
                    unique_data[key] = data[key]

            if not len(unique_data.keys()):
                raise Exception('cannot check if this model exists locally')

        try:
            model = model_class.objects.get(**unique_data)
        except model_class.DoesNotExist:
            model = model_class(**unique_data)

        for key, value in data.items():
            is_string = isinstance(value, six.string_types)
            field = model_class._meta.get_field_by_name(key)[0]

            if getattr(field, 'rel', None) and is_string:
                setattr(model, key, self.download(value))
            else:
                setattr(model, key, value)

        model.save()

        return model
