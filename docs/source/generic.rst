GenericForeignKey support
=========================

Generic foreign keys are supported since 0.4.

GenericChannelBase
------------------

.. automodule:: autocomplete_light.channel.generic
   :members:

Example
~~~~~~~

.. literalinclude:: ../../test_api_project/project_specific/generic_channel_example.py
   :language: python

GenericForeignKeyField
----------------------

.. automodule:: autocomplete_light.generic
   :members:

Example
~~~~~~~

.. literalinclude:: ../../test_api_project/project_specific/generic_form_example.py
   :language: python

GenericManyToMany
-----------------

.. automodule:: autocomplete_light.contrib.generic_m2m
   :members:

Example
~~~~~~~

Example model with ``related``:

.. literalinclude:: ../../test_project/generic_m2m_example/models.py
   :language: python

Example ``generic_m2m.GenericModelForm`` usage:

.. literalinclude:: ../../test_project/generic_m2m_example/forms.py
   :language: python

Example ``ModelAdmin``:

.. literalinclude:: ../../test_project/generic_m2m_example/admin.py
   :language: python
