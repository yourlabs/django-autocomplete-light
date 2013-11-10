Form, fields and widgets
========================

Design documentation
--------------------

This app provides optionnal helpers to make forms:

- :py:func:`autocomplete_light.modelform_factory <autocomplete_light.forms.modelform_factory>` 
  which wraps around django's modelform_factory but uses the heroic
  :py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.ModelForm>`.
- :py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.ModelForm>`: 
  the heroic ModelForm which couples all our loosely coupled tools together.
  For an exhaustive list of tools that it uses and that you can re-use
  (particularely if you don't want to or can't use the provided ModelForm),
  refer to :ref:`the Form API doc <form-api>`.

You probably already know that Django has form-fields for validation and each
form-field has a widget for rendering logic.

:py:class:`autocomplete_light.FieldBase <autocomplete_light.fields.FieldBase>`
makes a form field field rely on an Autocomplete class for initial choices and
validation (hail DRY configuration !), it is used as a mixin to make some
simple field classes:

    - :py:class:`autocomplete_light.ModelChoiceField <autocomplete_light.fields.ModelChoiceField>`,
    - :py:class:`autocomplete_light.ModelMultipleChoiceField <autocomplete_light.fields.ModelMultipleChoiceField>`,
    - :py:class:`autocomplete_light.GenericModelChoiceField <autocomplete_light.fields.GenericModelChoiceField>`, and
    - :py:class:`autocomplete_light.GenericModelMultipleChoiceField <autocomplete_light.fields.GenericModelMultipleChoiceField>`.

In the very same fashion, :py:class:`autcomplete_light.WidgetBase <autocomplete_light.widgets.WidgetBase>` 
renders a template which should contain:

- a hidden ``<select>`` field containing real field values,
- a visible ``<input>`` field which has the autocomplete,
- a deck which contains the list of selected values,
- add-another optionnal link, because add-another works outside the admin,
- a hidden choice template, which is copied when a choice is created on the fly
  (ie. with add-another).

It is used as a mixin to make some simple widget classes:

- :py:class:`autocomplete_light.ChoiceWidget <autocomplete_light.widgets.ChoiceWidget>`,
- :py:class:`autocomplete_light.MultipleChoiceWidget <autocomplete_light.widgets.MultipleChoiceWidget>`,
- :py:class:`autocomplete_light.TextWidget <autocomplete_light.widgets.TextWidget>`.

Examples
--------

ModelForm and Meta options
``````````````````````````

By default, :py:class:

.. code-block:: python

    class OrderForm(autocomplete_light.ModelForm):
        class Meta:
            model = Order

Enabling autocomplete for specific fields
`````````````````````````````````````````

.. code-block:: python

    class OrderForm(autocomplete_light.ModelForm):
        class Meta:
            model = Order
            autocomplete_fields = ['person']

Excluding autocomplete for specific fields
``````````````````````````````````````````

.. code-block:: python

    class OrderForm(autocomplete_light.ModelForm):
        class Meta:
            model = Order
            autocomplete_exclude = ['person']

Or in a ``ModelChoiceField`` or similar
```````````````````````````````````````

Now use ``PersonAutocomplete`` in a ``ChoiceWidget`` ie. for a ``ForeignKey``,
it can look like this:

.. code-block:: python

    from django import forms

    import autocomplete_light

    from models import Order, Person

    class OrderForm(forms.ModelForm):
        person = forms.ModelChoiceField(Person.objects.all(),
            widget=autocomplete_light.ChoiceWidget('PersonAutocomplete'))

        class Meta:
            model = Order

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

Using autocomplete widgets in non model-forms
`````````````````````````````````````````````

There are 3 kinds of widgets:

- ``autocomplete_light.ChoiceWidget`` has a hidden ``<select>`` which works for
  ``django.forms.ChoiceField``,
- ``autocomplete_light.MultipleChoiceWidget`` has a hidden ``<select
  multiple="multiple">`` which works for ``django.forms.MultipleChoiceField``,
- ``autocomplete_light.TextWidget`` just enables an autocomplete on its
  ``<input>`` and works for ``django.forms.CharField``.

For example:

.. code-block:: python

    # Using widgets directly in any kind of form.
    class NonModelForm(forms.Form):
        user = forms.ModelChoiceField(User.objects.all(),
            widget=autocomplete_light.ChoiceWidget('UserAutocomplete'))

        cities = forms.ModelMultipleChoiceField(City.objects.all(),
            widget=autocomplete_light.MultipleChoiceWidget('CityAutocomplete'))

        tags = forms.CharField(
            widget=autocomplete_light.TextWidget('TagAutocomplete'))

Overriding a JS option in Python
````````````````````````````````

Javascript widget options can be set in Python via the ``widget_js_attributes``
keyword argument. And javascript autocomplete options can be set in Python via
the ``autocomplete_js_attributes``.

Those can be set either on an Autocomplete class, either using the
``register()`` shortcut, either via the Widget constructor.

Per Autocomplete class
>>>>>>>>>>>>>>>>>>>>>>

.. code-block:: python
    
    class AutocompleteYourModel(autocomplete_light.AutocompleteModelTemplate):
        template_name = 'your_app/your_special_choice_template.html'

        autocomplete_js_attributes = {
            # This will actually data-autocomplete-minimum-characters which
            # will set widget.autocomplete.minimumCharacters.
            'minimum_characters': 4, 
        }

        widget_js_attributes = {
            # That will set data-max-values which will set widget.maxValues
            'max_values': 6,
        }

Per registered Autocomplete
>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. code-block:: python

    autocomplete_light.register(City,
        # Those have priority over the class attributes
        autocomplete_js_attributes={
            'minimum_characters': 0, 
            'placeholder': 'City name ?',
        }
        widget_js_attributes = {
            'max_values': 6,
        }
    )

Per widget
>>>>>>>>>>

.. code-block:: python

    class SomeForm(forms.Form):
        cities = forms.ModelMultipleChoiceField(City.objects.all(),
            widget=autocomplete_light.MultipleChoiceWidget('CityAutocomplete',
                # Those attributes have priority over the Autocomplete ones.
                autocomplete_js_attributes={'minimum_characters': 0,
                                            'placeholder': 'Choose 3 cities ...'},
                widget_js_attributes={'max_values': 3}))


API
---

Widgets
```````

.. automodule:: autocomplete_light.widgets

WidgetBase
>>>>>>>>>>

.. autoclass:: autocomplete_light.widgets.WidgetBase
   :members:

ChoiceWidget
>>>>>>>>>>>>

.. autoclass:: autocomplete_light.widgets.ChoiceWidget
   :members:

MultipleChoiceWidget
>>>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.widgets.MultipleChoiceWidget
   :members:

TextWidget
>>>>>>>>>>

.. autoclass:: autocomplete_light.widgets.TextWidget
   :members:

Fields
``````

.. automodule:: autocomplete_light.fields

FieldBase
>>>>>>>>>

.. autoclass:: autocomplete_light.fields.FieldBase

ModelChoiceField
>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.fields.ModelChoiceField
   :members:

ModelMultipleChoiceField
>>>>>>>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.fields.ModelMultipleChoiceField
   :members:

GenericModelChoiceField
>>>>>>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.fields.GenericModelChoiceField
   :members:

GenericModelMultipleChoiceField
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.fields.GenericModelMultipleChoiceField
   :members:

.. _form-api:

Form stuff
``````````

.. automodule:: autocomplete_light.forms

modelform_factory
>>>>>>>>>>>>>>>>>

.. autofunction:: autocomplete_light.forms.modelform_factory

ModelForm
>>>>>>>>>

.. autoclass:: autocomplete_light.forms.ModelFormMetaclass
   :members:

SelectMultipleHelpTextRemovalMixin
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.forms.SelectMultipleHelpTextRemovalMixin
   :members:

VirtualFieldHandlingMixin
>>>>>>>>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.forms.VirtualFieldHandlingMixin
   :members:

GenericM2MRelatedObjectDescriptorHandlingMixin
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.forms.GenericM2MRelatedObjectDescriptorHandlingMixin
   :members:

FormfieldCallback
>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.forms.FormfieldCallback
   :members:

ModelFormMetaclass
>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.forms.ModelFormMetaclass
   :members:
