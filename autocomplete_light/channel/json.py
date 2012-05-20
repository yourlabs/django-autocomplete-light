from django.utils import simplejson

from base import ChannelBase

__all__ = ('JSONChannelBase', )


class JSONChannelBase(ChannelBase):
    """
    Example channel that attaches JSON to results.
    """
    textarea = u'<textarea style="display:none">%s</textarea>'

    def result_as_html(self, result, extra_context=None):
        """
        Adds the return value of result_as_json() to the context.
        """
        return super(JSONChannelBase, self).result_as_html(result, {
            'extra_html': self.textarea % self.result_as_json(result)})

    def result_as_dict(self, result):
        """
        Return the dict that should be passed as JSON for a result. Used by
        result_as_json().
        """
        return {'value': result.pk}

    def result_as_json(self, result):
        """
        Return the JSON to attach to a result, uses result_as_dict() by
        default.
        """
        return simplejson.dumps(self.result_as_dict(result))
