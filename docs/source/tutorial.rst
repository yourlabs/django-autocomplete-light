Quick start: adding simple autocompletes
========================================

.. _quick-start:

This tutorial guides you through the process of enabling autocomplete for a
simple form. We'll enable autocompletion for ``Person`` on the form of an
``Order`` model, i.e. we want to get autocompletion for ``Person`` objects when
we type the person's first or last name.

For this to work, we have to register an autocomplete for the ``Person`` model.
The autocomplete tells autocomplete-light how to render your autocompletion and
what model fields to search in (like ``first_name``, ``last_name``, ...).

When we have defined how a ``Person`` autocompletion should look like, we have
to enable it in the ``Order`` form. This is done by modifying the ``Order``
form so that autocomplete-light's special form fields are used instead of the
ones built into Django. autocomplete-light provides a handy wrapper around
Django's modelforms which makes this a very easy thing to do.

:py:func:`autocomplete_light.register() <autocomplete_light.registry.register>` shortcut to generate and register Autocomplete classes
--------------------------------------------------------------------------------------------------------------------------------------

.. _register:

Register an Autocomplete for your model in
``your_app/autocomplete_light_registry.py``, it can look like this:

.. code-block:: python

    import autocomplete_light.shortcuts as al
    from models import Person

    # This will generate a PersonAutocomplete class.
    al.register(Person,
        # Just like in ModelAdmin.search_fields.
        search_fields=['^first_name', 'last_name'],
        attrs={
            # This will set the input placeholder attribute:
            'placeholder': 'Other model name ?',
            # This will set the yourlabs.Autocomplete.minimumCharacters
            # options, the naming conversion is handled by jQuery.
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

.. note::

    If using **Django >= 1.7**, you might as well do :py:func:`register()
    <autocomplete_light.registry.register>` calls directly in your
    ``AppConfig.ready()`` as demonstrated in the example app:
    ``autocomplete_light.example_apps.app_config_without_registry_file``.

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
        form = autocomplete_light.modelform_factory(Order, fields='__all__')
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

Thread safety and security considerations
-----------------------------------------

This section demonstrates how to handle one of the most difficult - but common
- use case: allowing different users to use different objects in an
autocomplete. For example, you want users to only see and use ``Item``
objects which they are ``owner`` of with such a model:

.. code-block:: python

    class Item(models.Model):
        owner = models.ForeignKey('auth.User')

Filtering on the owner on the ``request.owner`` on autocomplete box rendering
can be done directly in
:py:meth:`autocomplete_light.autocomplete.AutocompleteBase.choices_for_request()`,
because :py:meth:`autocomplete_light.views.AutocompleteView.get` passes the
``request`` object:

.. digraph:: rendering

   "AutocompleteView.get" -> "autocomplete = autocomplete_class(request=request)" -> "autocomplete.autocomplete_html()" -> "autocomplete.choices_for_request()";

However, this is not enough for security, because it doesn't prevent a
malicious user from using a model id it can't see and submitting the form,
allowing them for example to see the unicode representation of an object it
shouldn't be able to see when opening the change form again.

Django's form validation completely excludes the request object by default, so
autocomplete-light does the same by default, and the validation process looks
like:

.. digraph:: validation

   "Field.clean()" -> "Field.validate()" -> "autocomplete = autocomplete_class(values=values)" -> "autocomplete.validate_values()" -> "autocomplete.choices_for_values()";

A hook was added in autocomplete-light 2.3.0 to use the request object in the
validation process. Set the request attribute on the field to enable it, ie::

    form = YourForm(request.POST)

    # This enables the hook, otherwise, Django's default validation will happen
    # in addition to ``choices_for_values()``
    form.fields['your_autocomplete_field'].request = request

    # Now the request object will be part of the field validation process, ie.
    # when triggered by:
    form.is_valid()

Once the hook is enabled, :py:meth:`autocomplete_light.fields.FieldBase.validate()` will:

- instanciate the autocomplete with the ``request`` object, allowing
  ``choices_for_request()`` to work,
- **override** the autocomplete ``.choices`` with the result of
  ``choices_for_request()`` in ``validate()`` **before** calling
  :py:meth:`~autocomplete_light.autocomplete.base.AutocompleteBase.validate_values()`.

Resulting in a chain of events like:

.. digraph:: validation

   "form.fields['your_field'].request = request" -> "Field.clean()" -> "Field.validate()" -> "autocomplete = autocomplete_class(values=values, request=request)"-> "autocomplete.choices = autocomplete.choices_for_request()"  -> "autocomplete.validate_values()" -> "autocomplete.choices_for_values()";

You can then rely on ``choices_for_request()`` to secure choices, ie.:

.. literalinclude:: ../../autocomplete_light/tests/autocomplete/secure_autocomplete.py

.. warning:: Please ensure that you really test your autocompletes for
             security if it's going to be used to flip choices depending on the
             user using the form: feel free to use
             ``tests/autocomplete/test_model_security.py`` as an example.
