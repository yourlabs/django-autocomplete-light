from django.utils import simplejson

from base import ChannelBase

__all__ = ('JSONChannelBase', )


class JSONChannelBase(ChannelBase):
    def __init__(self):
        if not self.result_template:
            self.result_template = [
                'autocomplete_light/result_%s.html' % self.__class__.__name__,
                'autocomplete_light/result_with_json.html',
            ]

        super(JSONChannelBase, self).__init__()

    def result_as_dict(self, result):
        return {'value': result.pk}

    def result_as_json(self, result):
        return simplejson.dumps(self.result_as_dict(result))
