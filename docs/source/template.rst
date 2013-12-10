.. _template:

Styling autocompletes
=====================

A complete autocomplete widget has three parts you can style individually:

- the autocomplete widget, rendered on the form,
- the autocomplete box, fetched by ajax,
- choices presented by both the autocomplete box and :ref:`widget deck
  <widget-template>`.

Note that a choice HTML element is copied from the autocomplete box into the
deck uppon selection. It is then appended a "remove" element, that will remove
the choice uppon click.

Styling choices
---------------

By default, choices are rendered by the :py:meth:`choice_html() 
<autocomplete_light.autocomplete.base.AutocompleteBase.choice_html>` method.
The result of this method will be used in the autocomplete box as well as in
the :ref:`widget deck <widget-template>`. There are three easy ways to
customize it:

- overriding :py:attr:`AutocompleteBase.choice_html_format <autocomplete_light.registry.AutocompleteBase.choice_html_format>`,
- overriding :py:meth:`AutocompleteBase.choice_html() <autocomplete_light.autocomplete.base.AutocompleteBase.choice_html()>`,
- or even with a template specified in :py:attr:`AutocompleteTemplate.choice_template <autocomplete_light.autocomplete.template.AutocompleteTemplate.choice_template>` 

Overriding :py:attr:`AutocompleteBase.choice_html_format <autocomplete_light.registry.AutocompleteBase.choice_html_format>`
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

The easiest and most limited way to change how a choice is rendered is
to override the :py:attr:`AutocompleteBase.choice_html_format
<autocomplete_light.registry.AutocompleteBase.choice_html_format>`
attribute.

For example:

.. code-block:: python

    class OsAutocomplete(autocomplete_light.AutocompleteListBase):
        choices = ['Linux', 'BSD', 'Minix']
        choice_html_format = u'<span class="block os" data-value="%s">%s</span>'

This will add the class ``os`` to choices.

Overriding :py:meth:`AutocompleteBase.choice_html() <autocomplete_light.autocomplete.base.AutocompleteBase.choice_html()>`
``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

Overriding :py:meth:`AutocompleteBase.choice_html()
<autocomplete_light.autocomplete.base.AutocompleteBase.choice_html()>`
enables changing the way choices are rendered.

For example:

.. code-block:: python

    class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
        choice_html_format = u'''
            <span class="block" data-value="%s"><img src="%s" /> %s</span>
        '''

        def choice_html(self, choice):
            return self.choice_html_format % (self.choice_value(choice),
                choice.profile_image.url, self.choice_label(choice))

Overriding :py:attr:`AutocompleteTemplate.choice_template <autocomplete_light.autocomplete.template.AutocompleteTemplate.choice_template>`
``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

Perhaps the coolest way to style choices is to use a template. Just set
:py:attr:`AutocompleteTemplate.choice_template
<autocomplete_light.autocomplete.template.AutocompleteTemplate.choice_template>`.
It is used by :py:meth:`AutocompleteTemplate.choice_html
<autocomplete_light.autocomplete.template.AutocompleteTemplate.choice_html>`:

.. code-block:: python

    class PersonAutocomplete(autocomplete_light.AutocompleteModelTemplate):
        choice_template = 'person_choice.html'

Now, all you have to do is create a ``person_choice.html`` template. Consider
this elaborated example with image and links to the detail page and admin
change form:

.. code-block:: django

    {% load i18n %}
    {% load thumbnail %}

    <span class="block person" data-value="{{ choice.pk }}">
        <img src="{% thumbnail choice.profile_image.url 50x50 crop %}" />

        <a href="{{ choice.get_absolute_url }}">
            {{ choice.first_name }} {{ choice.last_name }}
        </a>
        
        <a href="{% url 'admin:persons_person_change' choice.pk %}">
            {% trans 'Edit person' %}
        </a>

        {% if choice.company %}
        <a href="{{ choice.get_absolute_url }}">
            {{ choice.company }}
        </a>
        {% endif %}
    </span>

First, the template loads the ``i18n`` template tags library which enables the
``{% trans %}`` template tag, useful for internationalization.

Then, it defines the ``<span>`` tag, this element is valid anywhere even if
your autocomplete widget is rendered in a ``<table>``. However, this ``<span>``
element has the ``block`` class which makes it ``display: block`` for space.
Also, it adds the ``person`` class to enable specific CSS stylings. Finally it
defines the ``data-value`` attribute. Note that **the ``data-value`` is
critical** because it is what tells ``autocomplete.js`` that this element is a
choice, and it also tells ``widget.js`` that the value is ``{{ choice.pk }}``
(which will be rendered before ``widget.js`` gets its hands on it of course).

Styling autocomplete boxes
--------------------------

By default, the autocomplete box is rendered by the :py:meth:`autocomplete_html() 
<autocomplete_light.autocomplete.base.AutocompleteBase.autocomplete_html>` method.
The result of this method will be used to render the autocomplete box. There
are many ways to customize it:

- overriding :py:attr:`AutocompleteBase.autocomplete_html_format <autocomplete_light.registry.AutocompleteBase.autocomplete_html_format>`,
- overriding :py:meth:`AutocompleteBase.autocomplete_html() <autocomplete_light.autocomplete.base.AutocompleteBase.autocomplete_html()>`,
- or even with a template specified in :py:attr:`AutocompleteTemplate.autocomplete_template <autocomplete_light.autocomplete.template.AutocompleteTemplate.autocomplete_template>` 
  if using :py:class:`AutocompleteTemplate <autocomplete_light.autocomplete.template.AutocompleteTemplate>` for rendering logic.

Overriding :py:attr:`AutocompleteBase.autocomplete_html_format <autocomplete_light.registry.AutocompleteBase.autocomplete_html_format>`
```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

The easiest and most limited way to change how a autocomplete is rendered is
to override the :py:attr:`AutocompleteBase.autocomplete_html_format
<autocomplete_light.registry.AutocompleteBase.autocomplete_html_format>`
attribute.

For example:

.. code-block:: python

    class OsAutocomplete(autocomplete_light.AutocompleteListBase):
        autocompletes = ['Linux', 'BSD', 'Minix']
        autocomplete_html_format = u'<span class="autocomplete-os">%s</span>'

This will add the ``autocomplete-os`` class to the autocomplete box.

Overriding :py:attr:`AutocompleteBase.autocomplete_html <autocomplete_light.registry.AutocompleteBase.autocomplete_html>`
`````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

Overriding :py:meth:`AutocompleteBase.autocomplete_html()
<autocomplete_light.autocomplete.base.AutocompleteBase.autocomplete_html()>`
enables changing the way autocompletes are rendered.

For example:

.. code-block:: python

    class PersonAutocomplete(autocomplete_light.AutocompleteModelBase):
        autocomplete_html_format = u'''
            <span class="autocomplete-os">
                <span class="count">%s Persons matching your query</span>
                %s
            </span>
        '''
        
        def autocomplete_html(self):
            html = ''.join(
                [self.choice_html(c) for c in self.choices_for_request()])

            if not html:
                html = self.empty_html_format % _('no matches found').capitalize()
            
            count = len(self.choices_for_request())
            return self.autocomplete_html_format % (count, html)

This will add a choice counter at the top of the autocomplete.

Overriding :py:attr:`AutocompleteTemplate.autocomplete_template <autocomplete_light.autocomplete.template.AutocompleteTemplate.autocomplete_template>`
``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

Perhaps the coolest way to style an autocomplete box is to use a template. Just set
:py:attr:`AutocompleteTemplate.autocomplete_template
<autocomplete_light.autocomplete.template.AutocompleteTemplate.autocomplete_template>`.
It is used by :py:meth:`AutocompleteTemplate.autocomplete_html
<autocomplete_light.autocomplete.template.AutocompleteTemplate.autocomplete_html>`:

.. code-block:: python

    class PersonAutocomplete(autocomplete_light.AutocompleteModelTemplate):
        autocomplete_template = 'person_autocomplete.html'

Now, all you have to do is create a ``person_autocomplete.html`` template.
Consider this elaborated example with user-friendly translated messages:

.. code-block:: django

    {% load i18n %}
    {% load autocomplete_light_tags %}

    {% if choices %}
        <h2>{% trans 'Please select a person' %}</h2>
        {% for choice in choices %}
            {{ choice|autocomplete_light_choice_html:autocomplete }}
        {% endfor %}
    {% else %}
        <h2>{% trans 'No matching person found' %}</h2>
        <p>
            {% blocktrans %}Sometimes, persons have not filled their name,
            maybe try to search based on email addresses ?{% endblocktrans %}
        </p>
    {% endif %}

First, it loads Django's i18n template tags for translation. Then, it loads
autocomplete-light's tags.

If there are any choices, it will display the list of choices, rendered by
``choice_html()`` through the ``autocomplete_light_choice_html`` template
filter as such: ``{{ choice|autocomplete_light_choice_html:autocomplete }}``.

If no choice is found, then it will display a user friendly suggestion.

Styling widgets
---------------

Widgets are rendered by the :py:meth:`~autocomplete_light.widgets.WidgetBase.render` 
method. By default, it renders `autocomplete_light/widget.html`. While you can
override the widget template globally, there are two ways to override the
widget template name on a per-case basis:

- :py:attr:`WidgetBase.widget_template <autocomplete_light.widgets.WidgetBase.widget_template>`,
- :py:attr:`AutocompleteBase.widget_template <autocomplete_light.registry.AutocompleteBase.widget_template>`,

Using another template instead of a global override allows to extend
the default widget template and override only the parts you need.

If you're not sure what is in a widget template, please review :ref:`part 2 of
reference documentation about widget templates<widget-template>`.

Also, note that the widget is styled with CSS, you can override or extend any
definition of ``autocomplete_light/style.css``.

:py:class:`~autocomplete_light.autocomplete.AutocompleteModelTemplate`
``````````````````````````````````````````````````````````````````````

By default,
:py:class:`~autocomplete_light.autocomplete.AutocompleteModelTemplate`
sets ``choice_template`` to
``autocomplete_light/model_template/choice.html``. It adds a "view
absolute url" link as well as an "update form url" link based on
``YourModel.get_absolute_url()`` and
``YourModel.get_absolute_update_url()`` with such a template:

.. literalinclude:: ../../autocomplete_light/templates/autocomplete_light/model_template/choice.html

It does not play well in all projects, so it was not set as default.
But you can inherit from it:

.. code-block:: python

    class YourAutocomplete(autocomplete_light.AutocompleteModelTemplate):
        model = YourModel
    autocomplete_light.register(YourAutocomplete)

Or let the :py:func:`~autocomplete_light.registry.register` shortcut
use it:

.. code-block:: python

    autocomplete_light.register(YourModel,
        autocomplete_light.AutocompleteModelTemplate)

Or set it as default with
:py:attr:`AutocompleteRegistry.autocomplete_model_base
<autocomplete_light.registry.AutocompleteRegistry.autocomplete_model_base>`
and used it as such:

.. code-block:: python

    autocomplete_light.register(YourModel)
