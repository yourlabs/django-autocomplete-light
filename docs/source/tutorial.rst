Enable an autocomplete in admin forms in two steps: high level API concepts
---------------------------------------------------------------------------

``register()`` shortcut to generate and register Autocomplete classes
`````````````````````````````````````````````````````````````````````

``register()`` passes the extra keyword arguments like ``search_fields`` to the
Python :py:func:``type`` function. This means that extra keyword arguments will
be used as class attributes of the generated class.

Register an Autocomplete for your model in
``your_app/autocomplete_light_registry.py``, it can look like this:

.. code-block:: python

    import autocomplete_light
    from models import Person

    # This will generate a PersonAutocomplete class
    autocomplete_light.register(Person, 
        # Just like in ModelAdmin.search_fields
        search_fields=['^first_name', 'last_name'],
        # This will actually data-minimum-characters which will set
        # widget.autocomplete.minimumCharacters.
        autocomplete_js_attributes={'placeholder': 'Other model name ?',},
    )

Because ``PersonAutocomplete`` is registered, ``AutocompleteView.get()`` can
proxy ``PersonAutocomplete.get()`` - and also ``AutocompleteView.post()`` to
``PersonAutocomplete.post()`` which is useful to build your own features using
Javascript method overrides.

This means that openning ``/autocomplete/PersonAutocomplete/`` will call
``AutocompleteView.get()`` which will in turn call
``PersonAutocomplete.get()``.

.. note::

    An equivalent way of doing the above is:

    .. code-block:: python

        class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
            search_fields = ['^first_name', 'last_name']
            autocomplete_js_attributes={'placeholder': 'Other model name ?',},
            model = Person
        autocomplete_light.register(PersonAutocomplete)

    If you wanted, you could override the default AutocompleteModelBase used by
    register() to generate Autocomplete classes. It looks like this (in urls.py):

    .. code-block:: python

        autocomplete_light.registry.autocomplete_model_base = YourAutocompleteModelBase
        autocomplete_light.autodiscover()

``modelform_factory()`` shortcut to generate ModelForms in the admin
````````````````````````````````````````````````````````````````````

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

.. note::

    There are two equivalent ways of doing this, using a ModelForm. They are
    described in later sections of this tutorial. After all, maybe you just
    wanted to replace Selects in the admin and autocomplete-light's job is done
    by now !

Making Autocomplete classes
---------------------------

Create a basic list-backed autocomplete class
`````````````````````````````````````````````

Registering a custom Autocomplete class for your model in
``your_app/autocomplete_light_registry.py`` can look like this:

.. code-block:: python

    import autocomplete_light

    class OsAutocomplete(autocomplete_light.AutocompleteListBase):
        choices = ['Linux', 'BSD', 'Minix']

    autocomplete_light.register(OsAutocomplete)

.. note::

    Class attributes are thread safe because ``register()`` always create a
    class copy.

Using a template to render the autocomplete
```````````````````````````````````````````

You could use :py:class:`autocomplete_light.AutocompleteListTemplate` instead:

.. code-block:: python

    import autocomplete_light

    class OsAutocomplete(autocomplete_light.AutocompleteListTemplate):
        choices = ['Linux', 'BSD', 'Minix']
        autocomplete_template = 'your_autocomplete_box.html'

    autocomplete_light.register(OsAutocomplete)

.. note::

    In reality, AutocompleteListBase inherits from both AutocompleteList and
    AutocompleteBase, and AutocompleteListTemplate inherits from both
    AutocompleteList and AutocompleteTemplate. It is the same for the other
    Autocomplete: AutocompleteModel + AutocompleteTemplate =
    AutocompleteModelTemplate and so on.

Create a basic model autocomplete class
````````````````````````````````````````

Registering a custom Autocomplete class for your model in
``your_app/autocomplete_light_registry.py`` can look like this:

.. code-block:: python

    import autocomplete_light

    from models import Person

    class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
        search_fields = ['^first_name', 'last_name']
    autocomplete_light.register(Person, PersonAutocomplete)

.. note::

    An equivalent of this example would be:

    .. code-block:: python
        
        autocomplete_light.register(Person, 
            search_fields=['^first_name', 'last_name'])

Overriding the queryset of a model autocomplete to secure an Autocomplete
`````````````````````````````````````````````````````````````````````````

You can override any method of the Autocomplete class. Filtering choices based on the request user could look like this:

.. code-block:: python

    import autocomplete_light

    from models import Person

    class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
        search_fields = ['^first_name', 'last_name'])

        def choices_for_request(self):
            choices = super(PersonAutocomplete, self).choices_for_request()

            if not self.request.user.is_staff:
                choices = choices.filter(private=False)

            return False

    autocomplete_light.register(Person, PersonAutocomplete)

Registering the same Autocomplete class for several autocompletes
`````````````````````````````````````````````````````````````````

This code registers an autocomplete with name 'ContactAutocomplete':

.. code-block:: python

    autocomplete_light.register(ContactAutocomplete)

To register two autocompletes with the same class, pass in a name argument:

.. code-block:: python
    
    autocomplete_light.register(ContactAutocomplete, name='Person', 
        choices=Person.objects.filter(is_company=False))
    autocomplete_light.register(ContactAutocomplete, name='Company',
        choices=Person.objects.filter(is_company=True))

Your own form classes
---------------------

Working around Django bug #9321: `Hold down "Control" ...`
``````````````````````````````````````````````````````````

If any autocomplete widget renders with a message like 'Hold down "Control" to
select multiple items at once', it is because of Django bug #9321. A trivial
fix is to use ``autocomplete_light.FixedModelForm``.

``FixedModelForm`` inherits from ``django.forms.ModelForm`` and only takes care
or removing this message. It remains compatible and can be used as a drop-in
replacement for ``ModelForm`.`

Of course, ``FixedModelForm`` is **not** required, but might prove helpful.

Override a default relation select in ``ModelForm.Meta.widgets``
````````````````````````````````````````````````````````````````

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
```````````````````````````````````````

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
```````````````````````````````````````

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

Using autocomplete widgets in non model-forms
`````````````````````````````````````````````

Any widget is usable in any form, ie.:

.. code-block:: python

    # Using widgets directly in any kind of form.
    class NonModelForm(forms.Form):
        user = forms.ModelChoiceField(User.objects.all(),
            widget=autocomplete_light.ChoiceWidget('UserAutocomplete'))

        cities = forms.ModelMultipleChoiceField(City.objects.all(),
            widget=autocomplete_light.MultipleChoiceWidget('CityAutocomplete'))

        tags = autocomplete_light.TextWidget('TagAutocomplete')

Overriding a JS option in Python
````````````````````````````````

Javascript widget options can be set in Python via the ``widget_js_attributes``
keyword argument. And javascript autocomplete options can be set in Python via
the ``autocomplete_js_attributes``.

Those can be set either on an Autocomplete class, either using the
``register()`` shortcut, either via the Widget constructor.

Per Autocomplete class
<<<<<<<<<<<<<<<<<<<<<<

.. code-block:: python
    
    class AutocompleteYourModel(autocomplete_light.AutocompleteModelTemplate):
        template_name = 'your_app/your_special_choice_template.html'

        autocomplete_js_attributes = {
            # This will actually data-autocomplete-minimum-characters which
            # will set widget.autocomplete.minimumCharacters.
            'minimum_characters': 4, 
        }

        widget_js_attributes = {
            # That will set data-max-values which will set widget.maxValues
            'max_values': 6,
        }

Per registered Autocomplete
<<<<<<<<<<<<<<<<<<<<<<<<<<<

.. code-block:: python

    autocomplete_light.register(City,
        # Those have priority over the class attributes
        autocomplete_js_attributes={
            'minimum_characters': 0, 
            'placeholder': 'City name ?',
        }
        widget_js_attributes = {
            'max_values': 6,
        }
    )

Per widget
<<<<<<<<<<

.. code-block:: python

    class SomeForm(forms.Form):
        cities = forms.ModelMultipleChoiceField(City.objects.all(),
            widget=autocomplete_light.MultipleChoiceWidget('CityAutocomplete',
                # Those attributes have priority over the Autocomplete ones.
                autocomplete_js_attributes={'minimum_characters': 0,
                                            'placeholder': 'Choose 3 cities ...'},
                widget_js_attributes={'max_values': 3}))

Javascript API concepts
-----------------------

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

Override autocomplete JS options in JS
``````````````````````````````````````

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

.. note::

    The pattern is the same for all plugins provided by django-autocomplete-light.

Override autocomplete JS methods
````````````````````````````````

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

.. note::

    The pattern is the same for all plugins provided by django-autocomplete-light.

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

Overriding widget JS methods
````````````````````````````

The widget js plugin will only bootstrap widgets which have
``data-bootstrap="normal"``. Which means that you should first name your new
bootstrapping method to ensure that the default behaviour doesn't get in the
way. 

.. code-block:: python

    autocomplete_light.register(City, 
        widget_js_attributes={'bootstrap': 'your-custom-bootstrap'})

.. note::

    You could do this at various level, by setting the ``bootstrap`` argument
    on a widget instance, via ``register()`` or directly on an autocomplete
    class. See Overriding JS options in Python for details.

Now, you can instanciate the widget yourself like this:

.. code-block:: javascript

    $(document).bind('yourlabsWidgetReady', function() {
        $('.your.autocomplete-light-widget[data-bootstrap=your-custom-bootstrap]').live('initialize', function() {
            $(this).yourlabsWidget({
                // Override options passed to $.yourlabsAutocomplete() from here
                autocompleteOptions: {
                    url: '{% url "your_autocomplete_url" %}',
                    // Override any autocomplete option in this array if you want
                    choiceSelector: '[data-id]',
                },
                // Override some widget options, allow 3 choices:
                maxValues: 3,
                // or method:
                getValue: function(choice) {
                    // This is the method that returns the value to use for the
                    // hidden select option based on the HTML of the selected
                    // choice.
                    //  
                    // This is where you could make a non-async post request to
                    // this.autocomplete.url for example. The default is:
                    return choice.data('id')
                },
            })
        });
    });

You can use the remote autocomplete as an example.

.. note::

    You could of course call ``$.yourlabsWidget()`` directly, but using the
    ``yourlabsWidgetReady`` event takes advantage of the built-in
    DOMNodeInserted event: your widgets will also work with dynamically created
    widgets (ie. admin inlines).
