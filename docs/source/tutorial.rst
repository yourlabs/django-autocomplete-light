Tutorial
========

.. _quick-start:

:py:func:`autocomplete_light.register() <autocomplete_light.registry.register>` shortcut to generate and register Autocomplete classes
--------------------------------------------------------------------------------------------------------------------------------------

.. _register:

Register an Autocomplete for your model in
``your_app/autocomplete_light_registry.py``, it can look like this:

.. code-block:: python

    import autocomplete_light
    from models import Person

    # This will generate a PersonAutocomplete class
    autocomplete_light.register(Person, 
        # Just like in ModelAdmin.search_fields
        search_fields=['^first_name', 'last_name'],
        attrs={
            # This will set the input placeholder attribute:
            'placeholder': 'Other model name ?',
            # This will set the yourlabs.Autocomplete.minimumCharacters
            # options, the naming conversion is handled by jQuery
            'data-autocomplete-minimum-characters': 1,
        },
        # This will set the data-widget-maximum-values attribute on the
        # widget container element, and will be set to
        # yourlabs.Widget.maximumValues (jQuery handles the naming
        # conversion).
        widget_attrs={
            'data-widget-maximum-values': 4,
            # Enable modern-style widget !
            'class': 'modern-style',
        },
    )

:py:meth:`AutocompleteView.get()
<autocomplete_light.views.AutocompleteView.get>` can proxy
:py:meth:`PersonAutocomplete.autocomplete_html()
<autocomplete_light.autocomplete.base.AutocompleteInterface.autocomplete_html>`
because ``PersonAutocomplete`` is registered. This means that openning
``/autocomplete/PersonAutocomplete/`` will call
:py:meth:`AutocompleteView.get()
<autocomplete_light.views.AutocompleteView.get>` which will in turn call
:py:meth:`PersonAutocomplete.autocomplete_html()
<autocomplete_light.autocomplete.base.AutocompleteInterface.autocomplete_html>`.

.. digraph:: autocomplete

   "widget HTML" -> "widget JavaScript" -> "AutocompleteView" -> "autocomplete_html()";

Also :py:meth:`AutocompleteView.post()
<autocomplete_light.views.AutocompleteView.post>` would proxy
``PersonAutocomplete.post()`` if it was defined. It could be useful to build
your own features like on-the-fly object creation using :ref:`Javascript method
overrides <js-method-override>` like the :ref:`remote autocomplete <remote>`.

.. warning::

    Note that this would make **all** ``Person`` public. Fine tuning
    security is explained later in this tutorial in section :ref:`security`.

:py:func:`autocomplete_light.register() <autocomplete_light.registry.register>`
generates an Autocomplete class, passing the extra keyword arguments like
:py:attr:`AutocompleteModel.search_fields
<autocomplete_light.autocomplete.model.AutocompleteModel.search_fields>` to the
Python :py:func:`type` function. This means that extra keyword arguments will
be used as class attributes of the generated class. An equivalent version of
the above code would be:

.. code-block:: python

    class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
        search_fields = ['^first_name', 'last_name']
        model = Person
    autocomplete_light.register(PersonAutocomplete)

.. note::

    If you wanted, you could override the default
    :py:class:`AutocompleteModelBase
    <autocomplete_light.autocomplete.AutocompleteModelBase>` used by
    :py:func:`autocomplete_light.register()
    <autocomplete_light.registry.register>` to generate :py:class:`Autocomplete
    <autocomplete_light.autocomplete.base.AutocompleteInterface>` classes.

    It could look like this (in your project's ``urls.py``):

    .. code-block:: python

        autocomplete_light.registry.autocomplete_model_base = YourAutocompleteModelBase
        autocomplete_light.autodiscover()

Refer to the :doc:`autocomplete` documentation for details, it is the first
chapter of the :ref:`the reference documentation <reference>`.

:py:func:`autocomplete_light.modelform_factory() <autocomplete_light.forms.modelform_factory>` shortcut to generate ModelForms in the admin
-------------------------------------------------------------------------------------------------------------------------------------------

First, ensure that scripts are :ref:`installed in the admin base template <install-scripts-admin>`.

Then, enabling autocompletes in the admin is as simple as  overriding
:py:attr:`ModelAdmin.form
<django:django.contrib.admin.ModelAdmin.form>` in
``your_app/admin.py``. You can use the
:py:func:`~autocomplete_light.forms.modelform_factory` shortcut as
such:

.. code-block:: python

    class OrderAdmin(admin.ModelAdmin):
        # This will generate a ModelForm
        form = autocomplete_light.modelform_factory(Order)
    admin.site.register(Order)

Refer to the :doc:`form` documentation for other ways of making forms, it is
the second chapter of the :ref:`the reference documentation <reference>`.

:py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.ModelForm>` to generate Autocomplete fields, the DRY way
--------------------------------------------------------------------------------------------------------------------------

First, ensure that :ref:`scripts are properly installed in your
template <install-scripts>`.

Then, you can use :py:class:`autocomplete_light.ModelForm
<autocomplete_light.forms.ModelForm>` to replace automatic
:py:class:`~django:django.forms.Select` and
:py:class:`~django:django.forms.SelectMultiple` widgets which renders
``<select>`` HTML inputs by autocompletion widgets:

.. code-block:: python

    class OrderModelForm(autocomplete_light.ModelForm):
        class Meta:
            model = Order

Note that the first Autocomplete class registered for a model becomes the
default Autocomplete for that model. If you have registered several
Autocomplete classes for a given model, you probably want to use a different
Autocomplete class depending on the form using 
:py:attr:`Meta.autocomplete_names <autocomplete_light.forms.ModelForm.autocomplete_names>`:

.. code-block:: python

    class OrderModelForm(autocomplete_light.ModelForm):
        class Meta:
            autocomplete_names = {'company': 'PublicCompanyAutocomplete'}
            model = Order

:py:class:`autocomplete_light.ModelForm <autocomplete_light.forms.ModelForm>`
respects ``Meta.fields`` and ``Meta.exclude``. However, you can enable or
disable :py:class:`autocomplete_light.ModelForm
<autocomplete_light.forms.ModelForm>`'s behaviour in the same fashion with
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

Also, it will automatically enable autocompletes on generic foreign keys and
generic many to many relations if you have at least one generic Autocomplete
class register (typically an
:py:class:`~autocomplete_light.autocomplete.AutocompleteGenericBase`).

For more documentation, continue reading :ref:`the reference documentation
<reference>`.
