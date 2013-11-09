AutocompleteGeneric, for GenericForeignKey or GenericManyToMany
===============================================================

Generic relation support comes in two flavors:

- for django's generic foreign keys,
- and for django-generic-m2m's generic many to many in
  autocomplete_light.contrib.generic_m2m,

AutocompleteGeneric
-------------------

Example using :py:class:`AutocompleteGeneric
<autocomplete_light.autocomplete.generic.AutocompleteGeneric>` as shown in
``test_project/gfk_autocomplete/autocomplete_light_registry.py``:

.. literalinclude:: ../../test_project/gfk_autocomplete/autocomplete_light_registry.py
   :language: python

.. _generic-fk:

GenericModelForm and GenericModelChoiceField
--------------------------------------------

Example using :py:class:`GenericModelForm
<autocomplete_light.generic.GenericModelForm>` and
:py:class:`GenericModelChoiceField
<autocomplete_light.generic.GenericModelChoiceField>` as shown in
``test_project/gfk_autocomplete/forms.py``:

.. literalinclude:: ../../test_project/gfk_autocomplete/forms.py
   :language: python

.. _generic-m2m:

GenericManyToMany
-----------------

Example
~~~~~~~

Consider this example model with a generic many-to-many relation descriptor
``related`` as in ``test_project/generic_m2m_autocomplete/models.py``:

.. literalinclude:: ../../test_project/generic_m2m_autocomplete/models.py
   :language: python

Example :py:class:`GenericModelForm
<autocomplete_light.contrib.generic_m2m.GenericModelForm>` and
:py:class:`GenericModelMultipleChoiceField
<autocomplete_light.contrib.generic_m2m.GenericModelMultipleChoiceField>` usage
as per ``test_project/generic_m2m_autocomplete/forms.py``:

.. literalinclude:: ../../test_project/generic_m2m_autocomplete/forms.py
   :language: python

The form defined above can directly be using in the admin:

.. literalinclude:: ../../test_project/generic_m2m_autocomplete/admin.py
   :language: python
