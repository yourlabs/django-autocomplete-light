Autocomplete classes
====================

.. note:: This chapter assumes that you have been through the entire
          :doc:`tutorial`.

.. _autocomplete-design:

Design documentation
--------------------

Any class which implements
:py:class:`~autocomplete_light.autocomplete.base.AutocompleteInterface` is
guaranteed to work because it provides the methods that are expected by the
view which serves autocomplete contents from ajax, and the methods that are
expected by the form field for validation and by the form widget for rendering. 

However, implementing those methods directly would result in duplicate code,
hence :py:class:`~autocomplete_light.autocomplete.base.AutocompleteBase`. It
contains all necessary rendering logic but lacks any business-logic, which
means that it is not connected to any data.

If you wanted to make an Autocomplete class that implements business-logic
based on a python list, you would end up with
:py:class:`~autocomplete_light.autocomplete.list.AutocompleteList`.

As you need both business-logic and rendering logic for an Autocomplete class
to be completely usable, you would mix both
:py:class:`~autocomplete_light.autocomplete.base.AutocompleteBase` and
:py:class:`~autocomplete_light.autocomplete.list.AutocompleteList` resulting in
:py:class:`~autocomplete_light.autocomplete.AutocompleteListBase`:

.. inheritance-diagram:: autocomplete_light.autocomplete.AutocompleteListBase
   :parts: 1

If you wanted to re-use your python list business logic with a template based
rendering logic, you would mix
:py:class:`~autocomplete_light.autocomplete.list.AutocompleteList` and
:py:class:`~autocomplete_light.autocomplete.template.AutocompleteTemplate`,
resulting in
:py:class:`~autocomplete_light.autocomplete.AutocompleteListTemplate`:

.. inheritance-diagram:: autocomplete_light.autocomplete.AutocompleteListTemplate
   :parts: 1

So far, you should understand that rendering and business logic are not coupled
in autocomplete classes: you can make your own business logic (ie.  using
redis, haystack ...) and re-use an existing rendering logic (ie.
:py:class:`~autocomplete_light.autocomplete.base.AutocompleteBase` or
:py:class:`~autocomplete_light.autocomplete.template.AutocompleteTemplate`) and
vice-versa.

For an exhaustive list of Autocomplete classes, refer to :ref:`the Autocomplete
API doc <autocomplete-api>`.

One last thing: Autocomplete classes should be :ref:`registered <register>` so
that the view can serve them and that form fields and widget be able to re-use
them. The registry itself is rather simple and filled with good intentions,
refer to :ref:`registry-api` documentation.

Examples
--------

.. _os-autocomplete:

Create a basic list-backed autocomplete class
`````````````````````````````````````````````

Class attributes are thread safe because
:py:func:`~autocomplete_light.registry.register`
always creates a class copy. Hence, registering a custom Autocomplete class for
your model in ``your_app/autocomplete_light_registry.py`` could look like this:

.. code-block:: python

    import autocomplete_light

    class OsAutocomplete(autocomplete_light.AutocompleteListBase):
        choices = ['Linux', 'BSD', 'Minix']

    autocomplete_light.register(OsAutocomplete)

First, we imported ``autocomplete_light``'s module. It should contain
everything you need.

Then, we subclassed :py:class:`autocomplete_light.AutocompleteListBase
<autocomplete_light.autocomplete.AutocompleteListBase>`, setting a list of
OSes in the
:py:attr:`~autocomplete_light.autocomplete.template.AutocompleteList.choices`
attribute.

Finally, we registered the Autocomplete class. It will be registered with the
class name by default.

.. note::

    Another way of achieving the above using the :ref:`register <register>`
    shortcut could be:
    
    .. code-block:: python
    
        autocomplete_light.register(autocomplete_light.AutocompleteListBase,
            name='OsAutocomplete', choices=['Linux', 'BSD', 'Minix'])

Using a template to render the autocomplete
```````````````````````````````````````````

You could use
:py:class:`~autocomplete_light.autocomplete.AutocompleteListTemplate` instead
of :py:class:`~autocomplete_light.autocomplete.AutocompleteListBase`:

.. code-block:: python

    import autocomplete_light

    class OsAutocomplete(autocomplete_light.AutocompleteListTemplate):
        choices = ['Linux', 'BSD', 'Minix']
        autocomplete_template = 'your_autocomplete_box.html'

    autocomplete_light.register(OsAutocomplete)

Inheriting from
:py:class:`~autocomplete_light.autocomplete.AutocompleteListTemplate` instead
of :py:class:`~autocomplete_light.autocomplete.AutocompleteListBase` like as
show in the **previous** example enables two optionnal options:

- :py:attr:`~autocomplete_light.autocomplete.template.AutocompleteTemplate.autocomplete_template` 
  which we have customized, if we hadn't then
  :py:meth:`AutocompleteTemplate.choice_html()
  <autocomplete_light.autocomplete.template.AutocompleteTemplate.choice_html>` would have fallen
  back on the parent :py:meth:`AutocompleteBase.choice_html()
  <autocomplete_light.autocomplete.base.AutocompleteBase.choice_html>`,
- :py:attr:`~autocomplete_light.autocomplete.template.AutocompleteTemplate.choice_template` 
  which we haven't set, so :py:meth:`AutocompleteTemplate.choice_html()
  <autocomplete_light.autocomplete.template.AutocompleteTemplate.choice_html>` will fall back on
  the parent :py:meth:`AutocompleteBase.choice_html()
  <autocomplete_light.autocomplete.base.AutocompleteBase.choice_html>`,

See :ref:`autocomplete-design` for details.

.. note:: 

    Another way of achieving the above could be:
    
    .. code-block:: python
    
        autocomplete_light.register(autocomplete_light.AutocompleteListTemplate,
            name='OsAutocomplete', choices=['Linux', 'BSD', 'Minix'],
            autocomplete_template='your_autocomplete_box.html')

Creating a basic model autocomplete class
`````````````````````````````````````````

Registering a custom Autocomplete class for your model in
``your_app/autocomplete_light_registry.py`` can look like this:

.. code-block:: python

    from models import Person

    class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
        search_fields = ['^first_name', 'last_name']
    autocomplete_light.register(Person, PersonAutocomplete)

In the same fashion, you could have used 
:py:class:`~autocomplete_light.autocomplete.AutocompleteModelTemplate`
instead of
:py:class:`~autocomplete_light.autocomplete.AutocompleteModelBase`. You can see
that the inheritance diagram follows the same pattern:

.. inheritance-diagram:: autocomplete_light.autocomplete.AutocompleteModelTemplate
   :parts: 1

.. note::

    An equivalent of this example would be:

    .. code-block:: python
        
        autocomplete_light.register(Person, 
            search_fields=['^first_name', 'last_name'])

.. _security:

Overriding the queryset of a model autocomplete to secure an Autocomplete
`````````````````````````````````````````````````````````````````````````

You can override any method of the Autocomplete class. Filtering choices based
on the request user could look like this:

.. code-block:: python

    class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
        search_fields = ['^first_name', 'last_name'])
        model = Person

        def choices_for_request(self):
            if not self.request.user.is_staff:
                self.choices = self.choices.filter(private=False)

            return super(PersonAutocomplete, self).choices_for_request()

    # we have specified PersonAutocomplete.model, so we don't have to repeat
    # the model class as argument for register()
    autocomplete_light.register(PersonAutocomplete)

It is very important to note here, that `clean()` **will** raise a
``ValidationError`` if a model is selected in a
``ModelChoiceField`` or ``ModelMultipleChoiceField`` 

.. note:: Use at your own discretion, as this can cause problems when a choice
          is no longer part of the queryset, just like with django's Select
          widget.

Registering the same Autocomplete class for several autocompletes
`````````````````````````````````````````````````````````````````

This code registers an autocomplete with name ``ContactAutocomplete``:

.. code-block:: python

    autocomplete_light.register(ContactAutocomplete)

To register two autocompletes with the same class, pass in a name argument:

.. code-block:: python
    
    autocomplete_light.register(ContactAutocomplete, name='Person', 
        choices=Person.objects.filter(is_company=False))
    autocomplete_light.register(ContactAutocomplete, name='Company',
        choices=Person.objects.filter(is_company=True))
