Tutorial
========

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

    class OrderAdmin(admin.ModelAdmin):
        # This will generate a ModelForm
        form = autocomplete_light.modelform_factory(Order)
    admin.site.register(Order)

There are other ways to generate forms, depending on your needs. Chances are
that you just wanted to replace selects in the admin then autocomplete-light's
job is done by now !

:py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.Modelform>` to generate Autocomplete fields, the DRY way
--------------------------------------------------------------------------------------------------------------------------

You can use :py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.Modelform>`
to replace automatic `<select>` fields with autocompletes:

.. code-block:: python

    class OrderModelForm(autocomplete_light.ModelForm):
        class Meta:
            model = Order

:py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.Modelform>`
respects ``Meta.fields`` and ``Meta.exclude``. However, you can enable or
disable :py:class:`autocomplete_light.ModelForm
<autocomplete_light.forms.Modelform>`'s behaviour in the same fashion with
:py:attr:`Meta.autocomplete_fields <autocomplete_light.forms.ModelForm.autocomplete_fields>`
and 
:py:attr:`Meta.autocomplete_exclude <autocomplete_light.forms.ModelForm.autocomplete_exclude>`:

.. code-block:: python

    class OrderModelForm(autocomplete_light.ModelForm):
        class Meta:
            model = Order
            # only enable autocompletes on 'person' and 'product' fields
            autocomplete_fields = ('person', 'product')

    class PersonModelForm(autocomplete_light.ModelForm):
        class Meta:
            model = Order
            # do not make 'category' an autocomplete field
            autocomplete_exclude = ('category',)

Also, it will
automatically enable autocompletes on generic foreign keys and generic many to
many relations if you have at least one generic Autocomplete class register
(typically an
:py:class:`~autocomplete_light.autocomplete.AutocompleteGenericBase`).

For more documentation, continue reading :ref:`the reference documentation
<reference>`.
