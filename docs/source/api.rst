.. _registry-api:

Registry API
============

.. automodule:: autocomplete_light.registry
   :members:

Autocomplete class API
======================

AutocompleteInterface
`````````````````````

.. autoclass:: autocomplete_light.autocomplete.base.AutocompleteInterface
   :members:

.. _autocomplete-api:

Rendering logic Autocomplete mixins
```````````````````````````````````

AutocompleteBase
>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.autocomplete.base.AutocompleteBase
   :members:

AutocompleteTemplate
>>>>>>>>>>>>>>>>>>>>

.. automodule:: autocomplete_light.autocomplete.template
   :members:

Business logic Autocomplete mixins
``````````````````````````````````

AutocompleteList
>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.autocomplete.list.AutocompleteList
   :members:

AutocompleteChoiceList
>>>>>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.autocomplete.choice_list.AutocompleteChoiceList
   :members:

AutocompleteModel
>>>>>>>>>>>>>>>>>

.. automodule:: autocomplete_light.autocomplete.model
   :members:

AutocompleteGeneric
>>>>>>>>>>>>>>>>>>>

.. automodule:: autocomplete_light.autocomplete.generic
   :members:

Autocomplete classes with both rendering and business logic
```````````````````````````````````````````````````````````

.. automodule:: autocomplete_light.autocomplete
   :members:
   :undoc-members:

Views
`````

.. automodule:: autocomplete_light.views
   :members:

Form, fields and widgets API
============================

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

ChoiceField
>>>>>>>>>>>

.. autoclass:: autocomplete_light.fields.ChoiceField
   :members:

MultipleChoiceField
>>>>>>>>>>>>>>>>>>>

.. autoclass:: autocomplete_light.fields.MultipleChoiceField
   :members:

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

.. autoclass:: autocomplete_light.forms.ModelForm
   :members:

ModelFormMetaclass
>>>>>>>>>>>>>>>>>>

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

Script API
==========

.. _autocomplete.js:

``autocomplete.js``
```````````````````

The autocomplete box script, see `autocomplete.js API documentation
<_static/autocomplete.html>`_.

``widget.js``
`````````````

The script that ties the autocomplete box script and the hidden ``<select>``
used by django, see `widget.js API documentation <_static/widget.html>`_.

``text_widget.js``
``````````````````

The script that ties the autocomplete box script with a text input, see
`text_widget.js API docummentation <_static/text_widget.html>`_.

``addanother.js``
`````````````````

The script that enables adding options to a ``<select>`` outside the admin, see
`addanother.js API documentation <_static/addanother.html>`_.

``remote.js``
`````````````

The script that overrides a method from ``widget.js`` to create choices on the
fly, see `remote.js API documentation <_static/remote.html>`_.
