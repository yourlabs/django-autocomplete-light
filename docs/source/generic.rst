AutocompleteGeneric, for GenericForeignKey or GenericManyToMany
===============================================================

Generic relation support comes in two flavors:

- for django's generic foreign keys,
- and for django-generic-m2m's generic many to many in
  autocomplete_light.contrib.generic_m2m,

AutocompleteGeneric
-------------------

Example
~~~~~~~

.. literalinclude:: ../../test_project/gfk_autocomplete/autocomplete_light_registry.py
   :language: python

API
~~~

.. autoclass:: autocomplete_light.autocomplete.generic.AutocompleteGeneric
   :members:

.. _generic-fk:

GenericModelChoiceField
-----------------------

Example
~~~~~~~

.. literalinclude:: ../../test_project/gfk_autocomplete/forms.py
   :language: python

API
~~~

.. automodule:: autocomplete_light.generic
   :members:

.. _generic-m2m:

GenericManyToMany
-----------------

Example
~~~~~~~

Example model with ``related``:

.. literalinclude:: ../../test_project/generic_m2m_autocomplete/models.py
   :language: python

Example ``generic_m2m.GenericModelForm`` usage:

.. literalinclude:: ../../test_project/generic_m2m_autocomplete/forms.py
   :language: python

Example ``ModelAdmin``:

.. literalinclude:: ../../test_project/generic_m2m_autocomplete/admin.py
   :language: python

API
~~~

.. automodule:: autocomplete_light.contrib.generic_m2m
   :members:
