Enable an autocomplete in admin forms: the two steps guide
----------------------------------------------------------

``register()`` shortcut can generate Autocomplete classes
`````````````````````````````````````````````````````````

Register an Autocomplete for your model in
``your_app/autocomplete_light_registry.py``, it can look like this:

  .. code-block:: python

    import autocomplete_light
    from models import Person

    # This will generate a PersonAutocomplete class
    autocomplete_light.register(Person, 
      search_fields=['^first_name', 'last_name'])

.. note::

    ``register()`` passes the extra keyword arguments like ``search_fields`` to
    the Python ``type()`` function. This means that extra keyword arguments
    will be used as class attributes of the generated class.

``modelform_factory()`` shortcut can generate ModelForms
````````````````````````````````````````````````````````

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

Using the autocomplete widget: low level API
--------------------------------------------

This chapter demonstrates how to achieve exactly the same thing than the
previous chapter: except that it doesn't take the shortcuts.

Your own Autocomplete class
```````````````````````````

Create a basic autocomplete class
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Registering a custom Autocomplete class for your model in
``your_app/autocomplete_light_registry.py`` can look like this:

  .. code-block:: python

    import autocomplete_light

    from models import Person

    class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
        search_fields = ['^first_name', 'last_name'])

        # here, you could override choices_for_request() for example if you
        # wanted to override how the queryset is constructed.

    autocomplete_light.register(Person, PersonAutocomplete)

Overriding the queryset of a model autocomplete
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Overriding javascript options from Python



Your own form classes
`````````````````````

Working around Django bug #9321: `Hold down "Control" ...`
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

If any autocomplete widget renders with a message like 'Hold down "Control" to
select multiple items at once', it is because of Django bug #9321. A trivial
fix is to use ``autocomplete_light.FixedModelForm``.

``FixedModelForm`` inherits from ``django.forms.ModelForm`` and only takes care
or removing this message. It remains compatible and can be used as a drop-in
replacement for ``ModelForm`.`

Of course, ``FixedModelForm`` is **not** required, but might prove helpful.

Override a default relation select in ``ModelForm.Meta.widgets``
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

You can override the default relation select as such:

  .. code-block:: python

    from django import forms

    import autocomplete_light

    from models import Order, Person

    class OrderForm(forms.ModelForm):
        class Meta:
            model = Order
            widgets = autocomplete_light.get_widgets_dict(Order)

Or in a ``ModelChoiceField`` or similar
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Now use ``PersonAutocomplete`` in a ``ChoiceWidget`` ie. for a ``ForeignKey``,
it can look like this:

  .. code-block:: python

    from django import forms

    import autocomplete_light

    from models import Order, Person

    class OrderForm(forms.ModelForm):
        person = forms.ModelChoiceField(Person.objects.all(),
            widget=autocomplete_light.ChoiceWidget('PersonAutocomplete'))

        class Meta:
            model = Order

Using your own form in a ``ModelAdmin``
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

You can use this form in the admin too, it can look like this:

  .. code-block:: python

    from django.contrib import admin
    
    from forms import OrderForm
    from models import Order

    class OrderAdmin(admin.ModelAdmin):
        form = OrderForm
    admin.site.register(Order, OrderAdmin)

.. note::

    Ok, this has nothing to do with ``django-autocomplete-light`` because it is
    plain Django, but still it might be useful to someone.

Javascript API
--------------

django-autocomplete-light provides consistent JS plugins. A concept that
you understand for one plugin is likely to be appliable for others.

Using ``$.yourlabsAutocomplete`` to create a navigation autocomplete
````````````````````````````````````````````````````````````````````

If you have a view that already renders just a list of links based on
``request.GET.q``, then you can use it to make a global navigation
autocomplete using ``autocomplete.js`` directly. It can look like this:

.. code-block:: javascript
    
    // Make a javascript Autocomplete object and set it up
    var autocomplete = $('#yourInput').yourlabsAutocomplete({
        url: '{% url "your_autocomplete_url" %}',
    });

So when the user clicks on a link of the autocomplete box which is generated by
your view: it is like if he clicked on a normal link.

.. note::

    This is because ``autocomplete.js`` is simple and stupid, it can't even
    generate an autocomplete box HTML ! But on the other hand you can use any
    server side caching or templates that you want ... So maybe it's a good thing ?

Using the ``choiceSelector`` option to enable keyboard navigation
`````````````````````````````````````````````````````````````````

Because the script doesn't know what HTML the server returns, it is nice to
tell it how to recognize choices in the autocomplete box HTML::

    $('#yourInput').yourlabsAutocomplete({
        url: '{% url "your_autocomplete_url" %}',
        choiceSelector: 'a',
    });

This will allow to use the keyboard arrows up/down to navigate between choices.

Using the ``selectChoice`` event to enable keyboard choice selection
````````````````````````````````````````````````````````````````````

``autocomplete.js`` doesn't do anything but trigger ``selectChoice`` on the
input when a choice is selected either with mouse **or keyboard**, let's enable
some action:

.. code-block:: javascript

    $('#yourInput').bind('selectChoice', function(e, choice, autocomplete) {
        window.location.href = choice.attr('href');
    });

.. note::

    Well, not only doesn't autocomplete.js generate the autocomplete box HTML, but
    it can't even do anything uppon choice selection ! What a stupid script. On the
    other hand it does allow to plug in radically different behaviours (ie.
    ModelChoiceWidget, TextWidget, ...) so maybe it's a good thing.

Combining the above to make a navigation autocomplete for mouse and keyboard
````````````````````````````````````````````````````````````````````````````

You've learned that you can have a fully functional navigation autocomplete
like on Facebook with just this:

.. code-block:: javascript

    $('#yourInput').yourlabsAutocomplete({
        url: '{% url "your_autocomplete_url" %}',
        choiceSelector: 'a',
    }).bind('selectChoice', function(e, choice, autocomplete) {
        window.location.href = choice.attr('href');
    });

Override js options
```````````````````

The array passed to the plugin function will actually be used to $.extend the
autocomplete instance, so you can override any option, ie:

.. code-block:: javascript

    $('#yourInput').yourlabsAutocomplete({
        url: '{% url "your_autocomplete_url" %}',
        // Hide after 200ms of mouseout
        hideAfter: 200,
        // Choices are elements with data-url attribute in the autocomplete
        choiceSelector: '[data-url]',
        // Show the autocomplete after only 1 character in the input.
        minimumCharacters: 1,
        // Override the placeholder attribute in the input:
        placeholder: '{% trans 'Type your search here ...' %}',
        // Append the autocomplete HTML somewhere else:
        appendAutocomplete: $('#yourElement'),
        // Override zindex:
        autocompleteZIndex: 1000,
    });

Override js methods
```````````````````
Overriding methods works the same, ie:

.. code-block:: javascript

    $('#yourInput').yourlabsAutocomplete({
        url: '{% url "your_autocomplete_url" %}',
        choiceSelector: '[data-url]',
        getQuery: function() {
            return this.input.val() + '&search_all=' + $('#searchAll').val();
        },
        hasChanged: function() {
            return true; // disable cache
        },
    });

Get an existing autocomplete object and chain autocompletes
```````````````````````````````````````````````````````````

You can use the jQuery plugin ``yourlabsAutocomplete()`` to get an existing
autocomplete object. Which makes chaining autocompletes with other form fields
as easy as:

.. code-block:: javascript
    
    $('#country').change(function() {
        $('#yourInput').yourlabsAutocomplete().data = {
            'country': $(this).val();
        }
    });
