Enable an autocomplete in admin forms in two steps: high level API concepts
===========================================================================

.. _quick-start:

:py:func:`autocomplete_light.register() <autocomplete_light.registry.register>` shortcut to generate and register Autocomplete classes
--------------------------------------------------------------------------------------------------------------------------------------

Register an Autocomplete for your model in
``your_app/autocomplete_light_registry.py``, it can look like this:

.. code-block:: python

    import autocomplete_light
    from models import Person

    # This will generate a PersonAutocomplete class
    autocomplete_light.register(Person, 
        # Just like in ModelAdmin.search_fields
        search_fields=['^first_name', 'last_name'],
        # This will actually html attribute data-placeholder which will set
        # javascript attribute widget.autocomplete.placeholder.
        autocomplete_js_attributes={'placeholder': 'Other model name ?',},
    )

Because ``PersonAutocomplete`` is registered, :py:meth:`AutocompleteView.get()
<autocomplete_light.views.AutocompleteView.get>` can proxy
:py:meth:`PersonAutocomplete.autocomplete_html()
<autocomplete_light.autocomplete.base.AutocompleteInterface.autocomplete_html>`.
This means that openning ``/autocomplete/PersonAutocomplete/`` will call
:py:meth:`AutocompleteView.get()
<autocomplete_light.views.AutocompleteView.get>` which will in turn call
:py:meth:`PersonAutocomplete.autocomplete_html()
<autocomplete_light.autocomplete.base.AutocompleteInterface.autocomplete_html>`.

Also :py:meth:`AutocompleteView.post()
<autocomplete_light.views.AutocompleteView.post>` would proxy
``PersonAutocomplete.post()`` if it was defined. It could be useful to build
your own features like on-the-fly object creation using :ref:`Javascript method
overrides <js-method-override>` like the :ref:`remote autocomplete <remote>`.

.. warning::

    Note that this would make **all** ``Person`` public. Fine tuning
    security is explained later in this tutorial in section :ref:`security`.

:py:func:`autocomplete_light.register() <autocomplete_light.registry.register>`
works by passing the extra keyword arguments like ``search_fields`` to the
Python :py:func:`type` function. This means that extra keyword arguments will
be used as class attributes of the generated class. An equivalent version of
the above code would be:

.. code-block:: python

    class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
        search_fields = ['^first_name', 'last_name']
        autocomplete_js_attributes={'placeholder': 'Other model name ?',}
        model = Person
    autocomplete_light.register(PersonAutocomplete)

.. note::

    If you wanted, you could override the default
    :py:class:`AutocompleteModelBase
    <autocomplete_light.autocomplete.AutocompleteModelBase>` used by
    :py:func:`autocomplete_light.register()
    <autocomplete_light.registry.register>` to generate :py:class:`Autocomplete
    <autocomplete_light.autocomplete.base.AutocompleteInterface>` classes.

    It could look like this (in urls.py):

    .. code-block:: python

        autocomplete_light.registry.autocomplete_model_base = YourAutocompleteModelBase
        autocomplete_light.autodiscover()

:py:func:`autocomplete_light.modelform_factory() <autocomplete_light.forms.modelform_factory>` shortcut to generate ModelForms in the admin
--------------------------------------------------------------------------------------------------------------------------------------------

Make the admin ``Order`` form that uses ``PersonAutocomplete``, in
``your_app/admin.py``:

.. code-block:: python

    from django.contrib import admin
    import autocomplete_light
    from models import Order

    class OrderAdmin(admin.ModelAdmin):
        # This will generate a ModelForm
        form = autocomplete_light.modelform_factory(Order)
    admin.site.register(Order)

There are other ways to generate forms, depending on your needs. If you just
wanted to replace selects in the admin then autocomplete_light's job is done by
now !

Else, continue reading :ref:`the reference documentation <reference>`.
