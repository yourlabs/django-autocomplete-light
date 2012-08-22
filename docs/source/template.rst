.. _template:

Templating autocompletes
========================

This documentation drives through the example app ``template_autocomplete``,
which is available in ``test_project``.

API
===

.. autoclass:: autocomplete_light.autocomplete.template.AutocompleteTemplate
   :members:

In ``autocomplete_light/autocomplete/__init__.py``, it is used as a mixin::

    class AutocompleteModelBase(AutocompleteModel, AutocompleteBase):
        pass


    class AutocompleteModelTemplate(AutocompleteModel, AutocompleteTemplate):
        pass

Example
=======

In this case, all you have to do, is use ``AutocompleteModelTemplate`` instead
of ``AutocompleteModelBase``. For example, in
``test_project/template_autocomplete/autocomplete_light_registry.py``:

.. literalinclude:: ../../test_project/template_autocomplete/autocomplete_light_registry.py
   :language: python


This example template makes choices clickable, it is
``test_project/template_autocomplete/templates/template_autocomplete/templated_choice.html``:

.. literalinclude:: ../../test_project/template_autocomplete/templates/template_autocomplete/templated_choice.html
   :language: django
