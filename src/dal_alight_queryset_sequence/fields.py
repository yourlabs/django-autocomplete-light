"""Autocomplete fields for AlightGenericForeignKey choices."""

from django.urls import re_path as url
from queryset_sequence import QuerySetSequence

from dal_alight_queryset_sequence.views import AlightQuerySetSequenceAutoView
from dal_alight_queryset_sequence.widgets import QuerySetSequenceAlight
from dal_queryset_sequence.fields import QuerySetSequenceModelField


class AlightGenericForeignKeyModelField(QuerySetSequenceModelField):
    """
    AlightGenericForeignKeyModelField class.

    Field that automatically generates the view for the
    :py:class:`~dal_alight_queryset_sequence.widgets.QuerySetSequenceAlight`
    widget.

    :param model_choice:
        ``[(Model, 'filter_by', [('forwardfield_name', 'filter_by')]), …]``

        List of tuples, one per model to include in the autocomplete.
        *Model* is the Django model class; ``'filter_by'`` is the field name
        used for ``icontains`` filtering.  The optional third element is a list
        of ``(forwarded_field_name, model_field_name)`` pairs for forwarding
        form fields to the view.
    :param field_id: Optional stable identifier; defaults to ``id(self)``.
    """

    def __init__(self, *args, **kwargs):
        """Initialize AlightGenericForeignKeyModelField."""
        model_choice = kwargs.pop('model_choice', None)
        field_id = kwargs.pop('field_id', None)
        self.field_id = field_id if field_id else id(self)
        if model_choice:
            self.model_choice = model_choice
            models_queryset = [model[0].objects.all()
                               for model in model_choice]
            kwargs['queryset'] = QuerySetSequence(*models_queryset)

        super(AlightGenericForeignKeyModelField, self).__init__(*args, **kwargs)

    def as_url(self, form):
        """Return url pattern for the auto-generated autocomplete view."""
        url_name = 'alight_{}_autocomp_{}'.format(form.__name__, self.field_id)

        forward_fields = {
            forward_tuple[0]
            for field in self.model_choice if len(field) > 2
            for forward_tuple in field[2]
        }
        # A set of the fields to forward.
        # It checks if the 3rd index of the list exists.

        self.widget = QuerySetSequenceAlight(
            url=url_name, forward=forward_fields
        )

        # Generate the class to work with multiple GFK
        # (can't work on instance level).
        auto_view = type(
            'Autoview{}{}'.format(form.__name__, self.field_id),
            (AlightQuerySetSequenceAutoView,),
            {'model_choice': self.model_choice}
        )  # Send to the view the model and filter list.

        return url(
            r'^alight_{}_{}_autocomp$'.format(form.__name__, self.field_id),
            auto_view.as_view(),
            name=url_name,
        )
