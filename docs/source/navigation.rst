Making a global navigation autocomplete
=======================================

This guide demonstrates how to make a global navigation autocomplete
like on http://betspire.com or facebook.

There is a living example in test_project/navigation_autocomplete, which this
page describes.

Note that there are many ways to implement such a feature, we're just
describing a simple one.

A simple view
-------------

As we're just going to use autocomplete.js for this, we only need a view to
render the autocomplete:

.. literalinclude:: ../../test_project/navigation_autocomplete/views.py

And a trivial template:

.. literalinclude:: ../../test_project/navigation_autocomplete/templates/navigation_autocomplete.html
   :language: django

And of course a url:

.. literalinclude:: ../../test_project/navigation_autocomplete/urls.py

A basic autocomplete configuration
----------------------------------

That's a pretty basic usage of autocomplete.js
(``test_project/navigation_autocomplete/templates/navigation_autocomplete_script.html``):

.. literalinclude:: ../../test_project/navigation_autocomplete/templates/navigation_autocomplete_script.html
   :language: django

Which works on such a simple input
(``test_project/navigation_autocomplete/templates/navigation_autocomplete_input.html``):

.. literalinclude:: ../../test_project/navigation_autocomplete/templates/navigation_autocomplete_input.html
   :language: django

See how ``admin/base_site.html`` includes them:

.. literalinclude:: ../../test_project/templates/admin/base_site.html
   :language: django
