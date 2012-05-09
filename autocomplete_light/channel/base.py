from django.core import urlresolvers
from django import template
from django.template import loader

__all__ = ('ChannelBase',)

class ChannelBase(object):
    model = None
    search_field = 'name'
    min_length = 0
    max_results = 20
    bootstrap = 'normal'

    def __init__(self):
        if hasattr(self.__class__, 'result_template'):
            self.result_template = self.__class__.result_template
        else:
            self.result_template = [
                'autocomplete_light/%s/result.html' % self.__class__.__name__.lower(),
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

    def query_filter(self, results):
        q = self.request.GET.get('q', None)

        if q:
            kwargs = { "%s__icontains" % self.search_field: q }
            results = results.filter(**kwargs)

        return results

    def values_filter(self, results, pks):
        results = results.filter(pk__in=pks)
        return results

    def get_queryset(self):
        return self.model.objects.all()

    def get_results(self, pks=None):
        results = self.get_queryset()

        if pks is not None:
            # used by the widget to prerender existing pks
            results = self.values_filter(results, pks)

        elif self.request:
            # used by the autocomplete
            results = self.query_filter(results)
        
        return self.order_results(results)
    
    def order_results(self, results):
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
        })

    def render_autocomplete(self):
        return self.render_to_string([
            'autocomplete_light/%s/autocomplete.html' % self.__class__.__name__.lower(),
            'autocomplete_light/autocomplete.html',
        ], {
            'channel': self,
        })
