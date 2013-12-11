Form, fields and widgets
========================

.. note:: This chapter assumes that you have been through 
          :doc:`tutorial` and :doc:`autocomplete`.

Design documentation
--------------------

This app provides optionnal helpers to make forms:

- :py:func:`autocomplete_light.modelform_factory <autocomplete_light.forms.modelform_factory>` 
  which wraps around django's modelform_factory but uses the heroic
  :py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.ModelForm>`.
- :py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.ModelForm>`: 
  the heroic ModelForm which ties all our loosely coupled tools together: 

    - :py:class:`~autocomplete_light.forms.SelectMultipleHelpTextRemovalMixin`,
      which removes the "Hold down control or command to select more
      than one" help text on autocomplete widgets (fixing `Django ticket #9321 
      <https://code.djangoproject.com/ticket/9321>`_),
    - :py:class:`~autocomplete_light.forms.VirtualFieldHandlingMixin`
      which enables support for generic foreign keys,
    - :py:class:`~autocomplete_light.forms.GenericM2MRelatedObjectDescriptorHandlingMixin`
      which enables support for generic many to many, if
      django-genericm2m is installed,
    - :py:class:`~autocomplete_light.forms.ModelFormMetaclass` which
      enables :py:class:`~autocomplete_light.forms.FormfieldCallback`
      to replace the default form field creator replacing `<select>`
      with autocompletes for relations and creates generic foreign key
      and generic many to many fields.

You probably already know that Django has form-fields for validation and each
form-field has a widget for rendering logic.

:py:class:`autocomplete_light.FieldBase <autocomplete_light.fields.FieldBase>`
makes a form field field rely on an Autocomplete class for initial choices and
validation (hail DRY configuration !), it is used as a mixin to make some
simple field classes:

    - :py:class:`autocomplete_light.ChoiceField <autocomplete_light.fields.ChoiceField>`,
    - :py:class:`autocomplete_light.MultipleChoiceField <autocomplete_light.fields.MultipleChoiceField>`,
    - :py:class:`autocomplete_light.ModelChoiceField <autocomplete_light.fields.ModelChoiceField>`,
    - :py:class:`autocomplete_light.ModelMultipleChoiceField <autocomplete_light.fields.ModelMultipleChoiceField>`,
    - :py:class:`autocomplete_light.GenericModelChoiceField <autocomplete_light.fields.GenericModelChoiceField>`, and
    - :py:class:`autocomplete_light.GenericModelMultipleChoiceField <autocomplete_light.fields.GenericModelMultipleChoiceField>`.

.. _widget-template: 

In the very same fashion, :py:class:`autcomplete_light.WidgetBase <autocomplete_light.widgets.WidgetBase>` 
renders a template which should contain:

- a hidden ``<select>`` field containing real field values,
- a visible ``<input>`` field which has the autocomplete,
- a **deck** which contains the list of selected values,
- add-another optionnal link, because add-another works outside the admin,
- a hidden choice template, which is copied when a choice is created on the fly
  (ie. with add-another).

It is used as a mixin to make some simple widget classes:

- :py:class:`autocomplete_light.ChoiceWidget <autocomplete_light.widgets.ChoiceWidget>`,
- :py:class:`autocomplete_light.MultipleChoiceWidget <autocomplete_light.widgets.MultipleChoiceWidget>`,
- :py:class:`autocomplete_light.TextWidget <autocomplete_light.widgets.TextWidget>`.

Examples
--------

This basic example demonstrates how to use an autocomplete form field in a form:

.. code-block:: python

    class YourForm(forms.Form):
        os = autocomplete_light.ChoiceField('OsAutocomplete')

Using :py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.Modelform>`
```````````````````````````````````````````````````````````````````````````````````

Consider such a model which have every kind of relations that are supported out
of the box:

.. code-block:: python

    class FullModel(models.Model):
        name = models.CharField(max_length=200)

        oto = models.OneToOneField('self', related_name='reverse_oto')
        fk = models.ForeignKey('self', related_name='reverse_fk')
        mtm = models.ManyToManyField('self', related_name='reverse_mtm')

        content_type = models.ForeignKey(ContentType)
        object_id = models.PositiveIntegerField()
        gfk = generic.GenericForeignKey("content_type", "object_id")

        # that's generic many to many as per django-generic-m2m
        gmtm = RelatedObjectsDescriptor()

Assuming that you have registered an ``Autocomplete`` for ``FullModel`` **and**
a generic ``Autocomplete``, then :py:class:`autocomplete_light.ModelForm
<autocomplete_light.forms.ModelForm>` will contain 5 autocompletion fields by
default: `oto`, `fk`, `mtm`, `gfk` and `gmtm`. 

.. code-block:: python

    class FullModelModelForm(autocomplete_light.ModelForm):
        class Meta:
            model = FullModel
            # add for django 1.6:
            fields = '__all__'

:py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.ModelForm>`
gives autocompletion super powers to :py:class:`django:django.forms.ModelForm`.
To disable the ``fk`` input for example:

.. code-block:: python

    class FullModelModelForm(autocomplete_light.ModelForm):
        class Meta:
            model = FullModel
            exclude = ['fk']

Or, to just get the default ``<select>`` widget for the ``fk`` field:

.. code-block:: python

    class FullModelModelForm(autocomplete_light.ModelForm):
        class Meta:
            model = FullModel
            autocomplete_exclude = ['fk']

In the same fashion, you can use ``Meta.fields`` and
``Meta.autocomplete_fields``. To the difference that they all understand
generic foreign key names and generic relation names in addition to regular
model fields.

Not using ``autocomplete_light.ModelForm``
``````````````````````````````````````````

Instead of using our :py:class:`autocomplete_light.ModelForm
<autocomplete_light.forms.ModelForm>`, you could create such a ModelForm using
our mixins:

.. code-block:: python

    class YourModelForm(autocomplete_light.SelectMultipleHelpTextRemovalMixin,
            autocomplete_light.VirtualFieldHandlingMixin,
            autocomplete_light.GenericM2MRelatedObjectDescriptorHandlingMixin,
            forms.ModelForm):
        pass

This way, you get a fully working ModelForm which does **not** handle any field
generation. You **can** use form fields directly though, which is demonstrated
in the next example.

Using form fields directly
``````````````````````````

You might want to use form fields directly for any reason:

- you don't want to or can't extend :py:class:`autocomplete_light.ModelForm
  <autocomplete_light.forms.ModelForm>`,
- you want to override a field, ie. if you have several Autocomplete classes
  registered for a model or for generic relations and you want to specify it,
- you want to override any option like placeholder, help_text and so on.

Considering the model of the above example, this is how you could do it:

.. code-block:: python
    
    class FullModelModelForm(autocomplete_light.ModelForm):
        # Demonstrate how to use a form field directly
        oto = autocomplete_light.ModelChoiceField('FullModelAutocomplete')
        fk = autocomplete_light.ModelChoiceField('FullModelAutocomplete')
        m2m = autocomplete_light.ModelMultipleChoiceField('FullModelAutocomplete')
        # It will use the default generic Autocomplete class by default
        gfk = autocomplete_light.GenericModelChoiceField()
        gmtm = autocomplete_light.GenericModelMultipleChoiceField()

        class Meta:
            model = FullModel
            # django 1.6:
            fields = '__all__'

As you see, it's as easy as 1-2-3, but keep in mind that this can break DRY:
:ref:`dry-break`.

Using your own form in a ``ModelAdmin``
```````````````````````````````````````

You can use this form in the admin too, it can look like this:

.. code-block:: python

    from django.contrib import admin
    
    from forms import OrderForm
    from models import Order

    class OrderAdmin(admin.ModelAdmin):
        form = OrderForm
    admin.site.register(Order, OrderAdmin)

.. note::

    Ok, this has nothing to do with ``django-autocomplete-light`` because it is
    plain Django, but still it might be useful to someone.
