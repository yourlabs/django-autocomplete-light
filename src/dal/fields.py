"""Form fields which may create missing models."""

from django import forms


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
