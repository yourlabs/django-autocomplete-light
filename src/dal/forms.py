"""
tl;dr: See FutureModelForm's docstring.

Many apps provide new related managers to extend your django models with. For
example, django-tagulous provides a TagField which abstracts an M2M relation
with the Tag model, django-gm2m provides a GM2MField which abstracts an
relation, django-taggit provides a TaggableManager which abstracts a relation
too, django-generic-m2m provides RelatedObjectsDescriptor which abstracts a
relation again.

While that works pretty well, it gets a bit complicated when it comes to
encapsulating the business logic for saving such data in a form object. This is
three-part problem:

- getting initial data,
- saving instance attributes,
- saving relations like reverse relations or many to many.

Django's ModelForm calls the model field's ``value_from_object()`` method to
get the initial data. ``FutureModelForm`` tries the ``value_from_object()``
method from the form field instead, if defined. Unlike the model field, the
form field doesn't know its name, so ``FutureModelForm`` passes it when calling
the form field's ``value_from_object()`` method.

Django's ModelForm calls the form field's ``save_form_data()`` in two
occasions:

- in ``_post_clean()`` for model fields in ``Meta.fields``,
- in ``_save_m2m()`` for model fields in ``Meta.virtual_fields`` and
  ``Meta.many_to_many``, which then operate on an instance which as a PK.

If we just added ``save_form_data()`` to form fields like for
``value_from_object()`` then it would be called twice, once in
``_post_clean()`` and once in ``_save_m2m()``. Instead, ``FutureModelForm``
would call the following methods from the form field, if defined:

- ``save_object_data()`` in ``_post_clean()``, to set object attributes for a
  given value,
- ``save_relation_data()`` in ``_save_m2m()``, to save relations for a given
  value.

For example:

- a generic foreign key only sets instance attributes, its form field would do
  that in ``save_object_data()``,
- a tag field saves relations, its form field would do that in
  ``save_relation_data()``.
"""

from itertools import chain

from django import forms


class FutureModelForm(forms.ModelForm):
    """
    ModelForm which adds extra API to form fields.

    Form fields may define new methods for FutureModelForm:

    - ``FormField.value_from_object(instance, name)`` should return the initial
      value to use in the form, overrides ``ModelField.value_from_object()``
      which is what ModelForm uses by default,
    - ``FormField.save_object_data(instance, name, value)`` should set instance
      attributes. Called by ``save()`` **before** writting the database, when
      ``instance.pk`` may not be set, it overrides
      ``ModelField.save_form_data()`` which is normally used in this occasion
      for non-m2m and non-virtual model fields.
    - ``FormField.save_relation_data(instance, name, value)`` should save
      relations required for value on the instance. Called by ``save()``
      **after** writting the database, when ``instance.pk`` is necessarely set,
      it overrides ``ModelField.save_form_data()`` which is normally used in
      this occasion for m2m and virtual model fields.

    For complete rationale, see this module's docstring.
    """

    def __init__(self, *args, **kwargs):
        """Override that uses a form field's ``value_from_object()``."""
        super(FutureModelForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if not hasattr(field, 'value_from_object'):
                continue

            self.initial[name] = field.value_from_object(self.instance, name)

    def _post_clean(self):
        """Override that uses the form field's ``save_object_data()``."""
        super(FutureModelForm, self)._post_clean()

        for name, field in self.fields.items():
            if not hasattr(field, 'save_object_data'):
                continue

            field.save_object_data(
                self.instance,
                name,
                self.cleaned_data.get(name, None),
            )

    def _save_m2m(self):  # noqa
        """Override that uses the form field's ``save_object_data()``."""
        cleaned_data = self.cleaned_data
        exclude = self._meta.exclude
        fields = self._meta.fields
        opts = self.instance._meta

        # Added to give the field a chance to do the work
        handled = []
        for name, field in self.fields.items():
            if not hasattr(field, 'save_relation_data'):
                continue

            field.save_relation_data(
                self.instance,
                name,
                cleaned_data[name]
            )

            handled.append(name)

        # Note that for historical reasons we want to include also
        # virtual_fields here. (GenericRelation was previously a fake
        # m2m field).
        virtual_fields = getattr(opts, 'virtual_fields', [])
        if not virtual_fields:
            virtual_fields = getattr(opts, 'private_fields', [])
        for f in chain(opts.many_to_many, virtual_fields):
            # Added to give the form field a chance to do the work
            if f.name in handled:
                continue

            if not hasattr(f, 'save_form_data'):
                continue
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if f.name in cleaned_data:
                f.save_form_data(self.instance, cleaned_data[f.name])

    def save(self, commit=True):
        """Backport from Django 1.9+ for 1.8."""
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance
