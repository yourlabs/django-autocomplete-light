Integration with forms
======================

The purpose of this documentation is to describe every element in a
chronological manner.

It is complementary with the quick documentation.

Django startup
--------------

.. _registry-reference:

Registry
~~~~~~~~

.. automodule:: autocomplete_light.registry
   :members:

.. _channel-reference:

Autocomplete basics
~~~~~~~~~~~~~~~~~~~

Examples
>>>>>>>>

Simple model autocomplete:

.. literalinclude:: ../../test_project/fk_autocomplete/autocomplete_light_registry.py
   :language: python

Slightly advanced autocomplete:

.. literalinclude:: ../../test_project/gfk_autocomplete/autocomplete_light_registry.py
   :language: python

API
>>>

.. autoclass:: autocomplete_light.autocomplete.base.AutocompleteInterface
   :members:

.. autoclass:: autocomplete_light.autocomplete.base.AutocompleteBase
   :members:

There are many autocompletes you can use, just to name a few:

- AutocompleteRestModelBase,
- AutocompleteGenericTemplate,
- AutocompleteModelTemplate,
- AutocompleteChoiceListBase ...

Each of them should have tests in autocomplete_light/tests and at least one
example app in test_project/.

Forms
~~~~~

.. Note::
    Due to `Django's issue #9321
    <https://code.djangoproject.com/ticket/9321>`_,
    you may have to use ``autocomplete_light.FixedModelForm`` instead of
    ``django.forms.ModelForm``. Otherwise, you might see help text like 'Hold
    down "Control" key ...' for MultipleChoiceWidgets.

API
>>>

A more high level API is also available:

.. automodule:: autocomplete_light.forms
   :members:

Page rendering
~~~~~~~~~~~~~~

It is important to load jQuery first, and then autocomplete_light and
application specific javascript, it can look like this::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
    {% include 'autocomplete_light/static.html' %}

However, ``autocomplete_light/static.html`` also includes "remote.js" which is
required only by remote channels. If you don't need it, you could either load
the static dependencies directly in your template, or override
``autocomplete_light/static.html``:

.. literalinclude:: ../../autocomplete_light/templates/autocomplete_light/static.html
   :language: django

Or, if you only want to make a global navigation autocomplete, you only need::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}autocomplete_light/autocomplete.js" type="text/javascript"></script>

.. include:: _admin_template.rst

.. _widget:

Widget in action
----------------

Widget definition
~~~~~~~~~~~~~~~~~

The first thing that happens is the definition of an AutocompleteWidget in a
form.


.. automodule:: autocomplete_light.widgets
   :members:

Example, overriding some `widget.js
<_static/widget.html>`_ and `autocomplete.js
<_static/autocomplete.html>`_ options directly from
Python:

.. literalinclude:: ../../test_project/docs_autocomplete/forms.py
   :language: python

Note that those have priority over those that are defined at the
autocomplete level:

.. literalinclude:: ../../test_project/docs_autocomplete/autocomplete_light_registry.py
   :language: python

Widget rendering
~~~~~~~~~~~~~~~~

This is what the default widget template looks like:

.. literalinclude:: ../../autocomplete_light/templates/autocomplete_light/widget.html
   :language: django

Javascript initialization
-------------------------

widget.js initializes all widgets that have bootstrap='normal' (the default),
as you can see::

    $('.autocomplete-light-widget[data-bootstrap=normal]').each(function() {
        $(this).autocompleteWidget();
    });

If you want to initialize the widget yourself, set the widget or channel
bootstrap to something else, say 'yourinit'. Then, add to
`yourapp/static/yourapp/autocomplete_light.js` something like::

    $('.autocomplete-light-widget[data-bootstrap=yourinit]').each(function() {
        $(this).yourlabs_widget({
            getValue: function(choice) {
                // your own logic to get the value from an html choice
                return ...;
            }
        });
    });

Also, load `yourapp/autocomplete_light.js` in your override of
autocomplete_light/static.html.

You should take a look at the docs of `autocomplete.js
<_static/autocomplete.html>`_
and `widget.js
<_static/widget.html>`_,
as it lets you override everything.

One interresting note is that the plugins (yourlabsAutocomplete and
autocompleteWidget) hold a registry. Which means that:

- calling someElement.autocompleteWidget() will instanciate a widget with the
  passed overrides
- calling someElement.autocompleteWidget() again will return the widget
  instance for someElement

This is exactly what you need to use to make autocompletes that depend on each
other.

Javascript cron
~~~~~~~~~~~~~~~

widget.js includes a javascript function that is executed every two seconds. It
checks each widget's hidden select for a value that is not in the widget, and
adds it to the widget if any.

This is useful for example, when an item was added to the hidden select via the
'+' button in django admin. But if you create items yourself in javascript and
add them to the select it would work too.

The reason for that is that adding and selecting an option from a select
doesn't trigger the javascript change event, which is a hudge pity.

.. _channel-view:

Javascript events
~~~~~~~~~~~~~~~~~

When the autocomplete input is focused, autocomplete.js checks if there are
enought caracters in the input to display an autocomplete box. If
minimumCharacters is 0, then it would open even if the input is empty, like a
normal select box.

If the autocomplete box is empty, it will fetch the autocomplete view. That
view delegates the rendering of the autocomplete box to the registered
autocomplete.

.. autoclass:: autocomplete_light.views.AutocompleteView
   :members:

.. automethod:: autocomplete_light.autocomplete.base.AutocompleteBase.autocomplete_html
   :noindex:

.. automethod:: autocomplete_light.autocomplete.base.AutocompleteBase.choice_html
   :noindex:

Then, autocomplete.js recognizes options with a selector. By default, it is
'[data-value]'. This means that any element with a data-value attribute in the
autocomplete html is considered a selectable choice.

When an option is selected, widget.js calls it's method getValue() and adds this
value to the hidden select. Also, it will copy the choice html to the widget.

When an option is removed from the widget, widget.js also removes it from the
hidden select.
