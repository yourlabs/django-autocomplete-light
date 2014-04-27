Voodoo black magic
------------------

This cookbook is a work in progress. Please report any error or things that
could be explained better ! And make pull requests heh ...

High level Basics
`````````````````

Various cooking recipes ``your_app/autocomplete_light_registry.py``:

.. code-block:: python

    # This actually creates a thread safe subclass of AutocompleteModelBase.
    autocomplete_light.register(SomeModel)

    # If NewModel.get_absolute_url or get_absolute_update_url is defined, this
    # will look more fancy
    autocomplete_light.register(NewModel,
        autocomplete_light.AutocompleteModelTemplate)

    # Extra **kwargs are used as class properties in the subclass.
    autocomplete_light.register(SomeModel,
        # SomeModel is already registered, re-register with custom name
        name='AutocompleteSomeModelNew',
        # Filter the queryset
        choices=SomeModel.objects.filter(new=True))

    # It is possible to override javascript options from Python.
    autocomplete_light.register(OtherModel,
        attrs={
            # This will actually data-autocomplete-minimum-characters which
            # will set widget.autocomplete.minimumCharacters.
            'data-autocomplete-minimum-characters': 0,
            'placeholder': 'Other model name ?',
        }
    )

    # But you can make your subclass yourself and override methods.
    class YourModelAutocomplete(autocomplete_light.AutocompleteModelTemplate):
        template_name = 'your_app/your_special_choice_template.html'

        attrs = {
            'data-mininum-minimum-characters': 4,
            'placeholder': 'choose your model',
        }

        widget_attrs = {
            # That will set widget.maximumValues, naming conversion is done by
            # jQuery.data()
            'data-widget-maximum-values': 6,
            'class': 'your-custom-class',
        }

        def choices_for_request(self):
            """ Return choices for a particular request """
            self.choices = self.choices.exclude(extra=self.request.GET['extra'])
            return super(YourModelAutocomplete, self).choices_for_request()

    # Just pass the class to register and it'll subclass it to be thread safe.
    autocomplete_light.register(YourModel, YourModelAutocomplete)

    # This will subclass the subclass, using extra kwargs as class attributes.
    autocomplete_light.register(YourModel, YourModelAutocomplete,
        # Again, registering another autocomplete for the same model, requires
        # registration under a different name
        name='YourModelOtherAutocomplete',
        # Extra **kwargs passed to register have priority.
        choice_template='your_app/other_template.html')

Various cooking recipes for ``your_app/forms.py``:

.. code-block:: python

    # Use as much registered autocompletes as possible.
    SomeModelForm = autocomplete_light.modelform_factory(SomeModel,
        exclude=('some_field'))

    # Same with a custom autocomplete_light.ModelForm
    class CustomModelForm(autocomplete_light.ModelForm):
        # autocomplete_light.ModelForm will set up the fields for you
        some_extra_field = forms.CharField()

        class Meta:
            model = SomeModel

    # Using form fields directly in any kind of form
    class NonModelForm(forms.Form):
        user = autocomplete_light.ModelChoiceField('UserAutocomplete')

        cities = autocomplete_light.ModelMultipleChoiceField('CityAutocomplete',
            widget=autocomplete_light.MultipleChoiceWidget('CityAutocomplete',
                # Those attributes have priority over the Autocomplete ones.
                attrs={'data-autocomplete-minimum-characters': 0,
                       'placeholder': 'Choose 3 cities ...'},
                widget_attrs={'data-widget-maximum-values': 3}))

        tags = forms.TextField(widget=autocomplete_light.TextWidget('TagAutocomplete'))

Low level basics
````````````````

This is something you probably won't need in the mean time. But it can turn out to be useful so here it is.

Various cooking recipes for ``autocomplete.js``, useful if you want to use it
manually for example to make a navigation autocomplete like facebook:

.. code-block:: js

    // Use default options, element id attribute and url options are required:
    var autocomplete = $('#yourInput').yourlabsAutocomplete({
        url: '{% url "your_autocomplete_url" %}'
    });

    // Because the jQuery plugin uses a registry, you can get the autocomplete
    // instance again by calling yourlabsAutocomplete() again, and patch it:
    $('#country').change(function() {
        $('#yourInput').yourlabsAutocomplete().data = {
            'country': $(this).val();
        }
    });
    // And that's actually how to do chained autocompletes.

    // The array passed to the plugin will actually be used to $.extend the
    // autocomplete instance, so you can override any option:
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

    // Or any method:
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

    // autocomplete.js doesn't do anything but trigger selectChoice when
    // an option is selected, let's enable some action:
    $('#yourInput').bind('selectChoice', function(e, choice, autocomplete) {
        window.location.href = choice.attr('href');
    });

    // For a simple navigation autocomplete, it could look like:
    $('#yourInput').yourlabsAutocomplete({
        url: '{% url "your_autocomplete_url" %}',
        choiceSelector: 'a',
    }).input.bind('selectChoice', function(e, choice, autocomplete) {
        window.location.href = choice.attr('href');
    });

Using `widget.js` is pretty much the same:

.. code-block:: js

    $('#yourWidget').yourlabsWidget({
        autocompleteOptions: {
            url: '{% url "your_autocomplete_url" %}',
            // Override any autocomplete option in this array if you want
            choiceSelector: '[data-id]',
        },
        // Override some widget options, allow 3 choices:
        maximumValues: 3,
        // or method:
        getValue: function(choice) {
            return choice.data('id'),
        },
    });

    // Supporting dynamically added widgets (ie. inlines) is
    // possible by using "solid initialization":
    $(document).bind('yourlabsWidgetReady', function() {
        $('.your.autocomplete-light-widget[data-bootstrap=your-custom-bootstrap]').live('initialize', function() {
            $(this).yourlabsWidget({
                // your options ...
            })
        });
    });
    // This method takes advantage of the default DOMNodeInserted observer
    // served by widget.js

There are some differences with `autocomplete.js`:

- widget expect a certain HTML structure by default,
- widget options can be overridden from HTML too,
- widget can be instanciated automatically via the default bootstrap

Hence the widget.js HTML cookbook:

.. code-block:: html

    <!--
    - class=autocomplete-light-widget: get picked up by widget.js defaults,
    - any data-widget-* attribute will override yourlabs.Widget js option,
    - data-widget-bootstrap=normal: Rely on automatic bootstrap because
      if don't need to override any method, but you could change
      that and make your own bootstrap, enabling you to make
      chained autocomplete, create options, whatever ...
    - data-widget-maximum-values: override a widget option maximumValues, note
      that the naming conversion is done by jQuery.data().
    -->
    <span
        class="autocomplete-light-widget"
        data-widget-bootstrap="normal"
        data-widget-maximum-values="3"
    >

        <!-- 
        Expected structure: have an input, it can set override default
        autocomplete options with data-autocomplete-* attributes, naming
        conversion is done by jQuery.data().
        -->
        <input 
            type="text" 
            data-autocomplete-minimum-characters="0"
            data-autocomplete-url="/foo" 
        />

        <!--
        Default expected structure: have a .deck element to append selected
        choices too:
        -->
        <span class="deck">
            <!-- Suppose a choice was already selected: -->
            <span class="choice" data-value="1234">Option #1234</span>
        </span>

        <!--
        Default expected structure: have a multiple select.value-select:
        -->
        <select style="display:none" class="value-select" name="your_input" multiple="multiple">
            <!-- If option 1234 was already selected: -->
            <option value="1234">Option #1234</option>
        </select>

        <!--
        Default expected structure: a .remove element that will be appended to
        choices, and that will de-select them on click:
        -->
        <span style="display:none" class="remove">Remove this choice</span>

        <!--
        Finally, supporting new options to be created directly in the select in
        javascript (ie. add another) is possible with a .choice-template. Of
        course, you can't take this very far, since all you have is the new
        option's value and html.
        -->
        <span style="display:none" class="choice-template">
            <span class="choice">
            </span>
        </span>
    </span>

Read everything about the registry and widgets.
