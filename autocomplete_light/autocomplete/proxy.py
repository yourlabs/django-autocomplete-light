from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django import http

__all__ = ['AutocompleteProxyInterface', 'AutocompleteProxy']


class AutocompleteProxyInterface(object):
    def choice_serialize(self, choice):
        """
        Serialize a choice so that it can be created upon selection.
        """
        raise NotImplemented()

    def choice_unserialize(self, text):
        """
        Return a value based on a seraliazed choice.
        """
        raise NotImplemented()

    def post(self, request):
        """
        Using a request with POST['choice'] containing a serialized choice,
        return an http response with the value of the serialized choice, as
        returned by choice_unserialize().
        """
        if 'choice' in request.POST.keys():
            choice_value = self.choice_unserialize(request.POST['choice'])
            return http.HttpResponse(choice_value, status=201)


class AutocompleteProxy(AutocompleteProxyInterface):
    def choice_serialize(self, choice):
        return simplejson.dumps(self.choice_dict(choice),
            cls=DjangoJSONEncoder)

    def choice_unserialize(self, text):
        return self.choice_dict_value(simplejson.loads(text))

    def choice_dict(self, choice):
        raise NotImplemented()

    def choice_dict_value(self, choice):
        raise NotImplemented()
