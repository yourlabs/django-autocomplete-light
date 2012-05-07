from django.utils import simplejson
from django.core import urlresolvers
from django import template
from django.template import loader

__all__ = ('ChannelBase',)

class ChannelBase(object):
    model = None
    search_field = 'name'
    min_length = 0
    max_results = 20

    def __init__(self):
        self.q = ''

        if hasattr(self.__class__, 'result_template'):
            self.result_template = self.__class__.result_template
        else:
            self.result_template = [
                'autocomplete_light/result_%s.html' % self.__class__.__name__,
                'autocomplete_light/result.html',
            ]

    def get_absolute_url(self):
        return urlresolvers.reverse('autocomplete_light_json_channel', args=(
            self.__class__.__name__,))
    
    def as_dict(self):
        return {
            'url': self.get_absolute_url(),
            'name': self.__class__.__name__
        }

    def init_for_request(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.q = self.parse_query()

    def parse_query(self):
        return self.request.GET.get('q', '')

    def get_queryset(self):
        return self.model.objects.all()

    def get_results(self, pks=None):
        results = self.get_queryset()
        if self.q: # used by the autocomplete
            kwargs = { "%s__icontains" % self.search_field: self.q }
            results = results.filter(**kwargs)
        if pks: # used by the widget to prerender existing pks
            results = results.filter(pk__in=pks)
        return results.order_by(self.search_field).distinct()[0:self.max_results]

    def are_valid(self, pks):
        return self.get_queryset().filter(pk__in=pks).count() == len(pks)

    def render_to_string(self, templates, context):
        if not isinstance(templates, (list, tuple)):
            templates = (templates,)

        return loader.select_template(templates).render(template.Context(context))

    def result_as_html(self, result):
        return self.render_to_string(self.result_template, {
            'channel': self, 
            'result': result,
            'result_dict_json': simplejson.dumps(self.result_as_dict(result)),
        })

    def result_as_json(self, result):
        return simplejson.dumps(self.result_as_dict(result))

    def result_as_dict(self, result):
        return {
            'value': result.pk,
        }

    def render_autocomplete(self):
        return self.render_to_string([
            'autocomplete_light/autocomplete_%s.html' % self.__class__.__name__,
            'autocomplete_light/autocomplete.html',
        ], {
            'channel': self,
        })
