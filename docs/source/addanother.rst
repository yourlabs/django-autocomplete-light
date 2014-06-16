.. _addanother:

Add another popup outside the admin
===================================

This documentation drives throught the example app ``non_admin_add_another`` which lives in
``test_project``.

Implementing this feature is utterly simple and can be done in two steps:

- make your create view to return some script if called with ``_popup=1``,
- add ``add_another_url_name`` attribute to your Autocomplete,

.. Warning::
    Note that this feature was added in version 1.0.21, if you have overloaded
    ``autocomplete_light/static.html`` from a previous version then you should
    make it load ``autocomplete_light/addanother.js`` to get this new feature.

Specifications
--------------

Consider such a model:

.. literalinclude:: ../../autocomplete_light/example_apps/non_admin_add_another/models.py

And we want to have add/update views outside the admin, with autocompletes for
relations as well as a ``+``/add-another button just like in the admin.

Technical details come from a blog post written by me a couple years ago,
`Howto: javascript popup form returning value for select like Django admin for
foreign keys
<http://blog.yourlabs.org/post/20001556462/howto-javascript-popup-form-returning-value-for-select>`_.

Create view
-----------

A create view opened via the add-another button should return such a body::

    <script type="text/javascript">
    opener.dismissAddAnotherPopup( 
        window, 
        "name of created model", 
        "id of created model" 
    );
    </script>

Note that you could also use ``autocomplete_light.CreateView`` which simply
wraps around ``django.views.generic.edit.CreateView.form_valid()`` to do that,
example usage:

.. literalinclude:: ../../autocomplete_light/example_apps/non_admin_add_another/urls.py

.. Note::
    It is not mandatory to use url namespaces.

Autocompletes
-------------

Simply register an Autocomplete for widget, with an ``add_another_url_name``
argument, for example:

.. literalinclude:: ../../autocomplete_light/example_apps/non_admin_add_another/autocomplete_light_registry.py
