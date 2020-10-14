"""View that supports QuerySetSequence."""

from dal.views import BaseQuerySetView

from django.contrib.contenttypes.models import ContentType

from queryset_sequence import QuerySetSequence


class BaseQuerySetSequenceView(BaseQuerySetView):
    """
    Base view that uses a QuerySetSequence.

    Compatible with form fields which use a ContentType id as well as a model
    pk to identify a value.

    .. py:attribute:: mixup

        Cause the autocomplete to show a few results of each querysets.
    """

    mixup = True
    paginate_by = 10

    def get_paginate_by(self, queryset):
        """Don't paginate if :py:attr:`mixup`."""
        return self.paginate_by if not self.mixup else None

    def has_more(self, context):
        """Return False if :py:attr:`mixup`."""
        if self.mixup:
            return False

        return super(BaseQuerySetSequenceView, self).has_more(context)

    def mixup_querysets(self, qs):
        """Return a queryset with different model types."""
        querysets = list(qs.get_querysets())
        queryset_count = len(querysets)
        if queryset_count:
            limit = int(self.paginate_by / queryset_count)
            qs = QuerySetSequence(*[q[:limit] for q in querysets])
        return qs

    def get_queryset(self):
        """Mix results from all querysets in QuerySetSequence if self.mixup."""
        qs = super(BaseQuerySetSequenceView, self).get_queryset()

        if self.mixup:
            qs = self.mixup_querysets(qs)

        return qs

    def get_result_value(self, result):
        """Return ctypeid-objectid for result."""
        return '%s-%s' % (ContentType.objects.get_for_model(result).pk,
                          result.pk)

    def get_model_name(self, model):
        """Return the name of the model, fetch parent if model is a proxy."""
        if model._meta.proxy:
            try:
                model = list(model._meta.parents.keys())[0]
            except IndexError:
                pass
        return model._meta.verbose_name
