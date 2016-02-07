"""Form fields which may create missing models."""

from django import forms


class FutureModelFieldMixin(object):
    def __init__(self, factory=None, *args, **kwargs):
        self._factory = factory
        choices = args[0] if len(args) else kwargs.get('queryset', None)

        if choices is None:
            args = ([],) + args

        super(FutureModelFieldMixin, self).__init__(*args, **kwargs)

    def _set_choices(self, choices):
        self._choices = choices

    def _get_choices(self):
        choices = getattr(self, '_choices', None)

        if choices is not None:
            return choices

        return forms.ModelChoiceIterator(self.queryset_factory())


    def queryset_factory(self):
        model_field = self._factory['meta'].model._meta.get_field_by_name(
            self.factory['field'].name)
        return model_field.rel.to.objects.all()

    def _set_widget(self):
        self._widget = widget

    def _get_widget(self):
        widget = getattr(self, '_widget', None)

        if widget is not None:
            return widget

        self._widget = self.widget_factory()
        return self._widget

    def widget_factory(self):
        return self.widget.factory(self)


class CreateModelFieldMixin(object):
    """Mixin for autocomplete form fields with create power."""

    def create_value(self, value):
        """Create and return a model from a user value."""
        return self.queryset.model.objects.create(name=value).pk

    def widget_attrs(self, widget):
        """Override to data-autocomplete-light-create to 'true'."""
        attrs = super(CreateModelFieldMixin, self).widget_attrs(widget)
        attrs['data-autocomplete-light-create'] = 'true'
        return attrs


class CreateModelField(CreateModelFieldMixin, forms.ModelChoiceField):
    """This field allows creating instances."""

    def clean(self, value):
        """Try the default clean method, else create if allowed."""
        try:
            return super(CreateModelFieldMixin, self).clean(value)
        except forms.ValidationError:
            if value:
                value = self.create_value(value)
            else:
                raise

        return super(CreateModelFieldMixin, self).clean(value)


class CreateModelMultipleField(CreateModelFieldMixin,
                               forms.ModelMultipleChoiceField):
    """This field allows creating instances."""

    def clean(self, value):
        """Try the default clean method, else create if allowed."""
        tries = len(value)

        while tries >= 0:
            try:
                return super(CreateModelMultipleField, self).clean(value)
            except forms.ValidationError as e:
                if e.params.get('pk', None):
                    new_value = self.create_value(e.params['pk'])
                    value[value.index(e.params['pk'])] = new_value
                else:
                    raise
            tries -= 1

        return super(CreateModelMultipleField, self).clean(value)
