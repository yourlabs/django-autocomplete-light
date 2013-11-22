.. _template:

Styling autocompletes
=====================

A complete autocomplete widget has three parts you can style individually:

- the autocomplete widget.
- the autocomplete box,
- choices presented by the autocomplete box,

Styling choices
---------------

By default, choices are rendered by the :py:meth:`choice_html() 
<autocomplete_light.autocomplete.base.AutocompleteBase.choice_html>` method.
The result of this method will be used in the autocomplete box as well as in
the :ref:`widget deck <widget-template>`. There are many ways to customize it:

- overriding :py:attr:`~autocomplete_light.autocomplete.base.AutocompleteBase.choice_html_format`,
- overriding :py:meth:`~autocomplete_light.autocomplete.base.AutocompleteBase.choice_html()`,
- or even with a template specified in :py:attr:`~autocomplete_light.autocomplete.template.AutocompleteTemplate.choice_template` 

For example:

.. code-block:: python

    class AutocompleteEditableModelBase(autocomplete_light.AutocompleteModelBase):
        choice_html_format = u'''
            <span class="div" data-value="%s">%s</span>
            <a href="%s" title="%s"><img src="%s%s" /></a>
        '''

        def choice_html(self, choice):
            """ 
            Return a choice formated according to self.choice_html_format.
            """
            return self.choice_html_format % ( 
                self.choice_value(choice), self.choice_label(choice),
                choice.get_absolute_update_url(), _(u'Update'),
                settings.STATIC_URL, 'admin/img/icon_changelink.gif')

    autocomplete_light.register(AppCategory, AutocompleteEditableModelBase,
        add_another_url_name='appstore_appcategory_create')

    autocomplete_light.register(AppFeature, AutocompleteEditableModelBase,
        add_another_url_name='appstore_appfeature_create')

Styling autocomplete boxes
--------------------------

By default, the autocomplete box is rendered by the :py:meth:`autocomplete_html() 
<autocomplete_light.autocomplete.base.AutocompleteBase.autocomplete_html>` method.
The result of this method will be used to render the autocomplete box. There
are many ways to customize it:

- overriding :py:attr:`~autocomplete_light.autocomplete.base.AutocompleteBase.autocomplete_html_format`,
- overriding :py:meth:`~autocomplete_light.autocomplete.base.AutocompleteBase.autocomplete_html()`,
- or even with a template specified in :py:attr:`~autocomplete_light.autocomplete.template.AutocompleteTemplate.autocomplete_template` 
  if using :py:class:`~autocomplete_light.autocomplete.template.AutocompleteTemplate` for rendering logic.

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

