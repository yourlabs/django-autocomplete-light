Dependencies between autocompletes
==================================

This means that the selected value in an autocomplete widget is used to filter
choices from another autocomplete widget.

This page drives through the example in autocomplete_light/example_apps/dependant_autocomplete/.

Specifications
--------------

Consider such a model:

.. literalinclude:: ../../autocomplete_light/example_apps/dependant_autocomplete/models.py

And we want two autocompletes in the form, and make the "region" autocomplete
to be filtered using the value of the "country" autocomplete.

Autocompletes
-------------

Register an Autocomplete for Region that is able to use 'country_id' GET
parameter to filter choices:

.. literalinclude:: ../../autocomplete_light/example_apps/dependant_autocomplete/autocomplete_light_registry.py

Javascript
----------

Actually, a normal modelform is sufficient. But it was decided to use
Form.Media to load the extra javascript:

.. literalinclude:: ../../autocomplete_light/example_apps/dependant_autocomplete/forms.py

That's the piece of javascript that ties the two autocompletes:

.. literalinclude:: ../../autocomplete_light/example_apps/dependant_autocomplete/static/dependant_autocomplete.js
   :language: javascript

Conclusion
----------

Again, there are many ways to acheive this. It's just a working example you can
test in the demo, you may copy it and adapt it to your needs.
