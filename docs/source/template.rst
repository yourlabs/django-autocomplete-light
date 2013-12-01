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

    <span class="block person" data-value="{{ choice.pk }}">
        <img src="{{ choice.profile_image.url }}" />

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

Styling widgets
---------------

Widgets are rendered by the :py:meth:`~autocomplete_light.widgets.WidgetBase.render` 
method. By default, it renders `autocomplete_light/widget.html`. You can set 
:py:attr:`~autocomplete_light.widgets.WidgetBase.template_name` to override it
or extend it on a per-widget basis.

Examples
--------

FTR, here's another way to do it, assuming your models have a
`get_absolute_update_url` method defined::

