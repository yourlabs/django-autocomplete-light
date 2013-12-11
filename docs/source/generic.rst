Generic relations
=================

Generic relation support comes in two flavors:

- for django's generic foreign keys,
- and for django-generic-m2m's generic many to many in
  autocomplete_light.contrib.generic_m2m,

In any case, you need to register an autocomplete class for generic
autocompletes.

The easiest is to inherit from
:py:class:`~autocomplete_light.autocomplete.AutocompleteGenericBase`
or
:py:class:`~autocomplete_light.autocomplete.AutocompleteGenericTemplate`. The
main logic is contained in
:py:class:`~autocomplete_light.autocomplete.generic.AutocompleteGeneric` which
is extended by both the Base and Template versions.

`autocomplete_light.ModelForm` will setup the fields:

- :py:class:`autocomplete_light.GenericModelChoiceField <autocomplete_light.fields.GenericModelChoiceField>`, and
- :py:class:`autocomplete_light.GenericModelMultipleChoiceField <autocomplete_light.fields.GenericModelMultipleChoiceField>`.

Those fields will use the default generic autocomplete class, which is the last
one you register as generic. If you want to use several generic autocomplete
classes, then you should setup the fields yourself to specify the autocomplete
name as such:

.. code-block:: python

    class YourModelForm(autocomplete_light.ModelForm):
        generic_fk = autocomplete_light.GenericModelChoiceField('YourAutocomplete1')
        generic_m2m = autocomplete_light.GenericModelMultipleChoiceField('YourAutocomplete2')

But please note that you will :ref:`loose some DRY<dry-break>` by doing that, as stated in the faq.

Example using :py:class:`~autocomplete_light.autocomplete.generic.AutocompleteGenericBase`
------------------------------------------------------------------------------------------

This example demonstrates how to setup a generic autocomplete with 4 models:

.. code-block:: python

    class AutocompleteTaggableItems(autocomplete_light.AutocompleteGenericBase):
        choices = (
            User.objects.all(),
            Group.objects.all(),
            City.objects.all(),
            Country.objects.all(),
        )

        search_fields = (
            ('username', 'email'),
            ('name',),
            ('search_names',),
            ('name_ascii',),
        )


    autocomplete_light.register(AutocompleteTaggableItems)
