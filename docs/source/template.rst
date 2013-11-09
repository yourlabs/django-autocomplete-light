.. _template:

Templating autocompletes
========================

This documentation drives through the example app
``test_project/template_autocomplete``.

You can use :py:class:`AutocompleteTemplate
<autocomplete_light.autocomplete.template.AutocompleteTemplate>` as a mixin
just like us:

.. code-block:: python

    class AutocompleteModelTemplate(AutocompleteModel, AutocompleteTemplate):
        pass

You could also directly inherit from :py:class:`AutocompleteModelTemplate
<autocomplete_light.autocomplete.AutocompleteModelTemplate>`.

Anyway, this enable two new attributes: :py:attr:`choice_template
<autocomplete_light.autocomplete.template.AutocompleteTemplate.choice_template>`
and :py:attr:`autocomplete_template
<autocomplete_light.autocomplete.template.AutocompleteTemplate.autocomplete_template>`

Example
-------

In this case, all you have to do, is use ``AutocompleteModelTemplate`` instead
of ``AutocompleteModelBase``. For example, in
``test_project/template_autocomplete/autocomplete_light_registry.py``:

.. literalinclude:: ../../test_project/template_autocomplete/autocomplete_light_registry.py
   :language: python


This example template makes choices clickable, it is
``test_project/template_autocomplete/templates/template_autocomplete/templated_choice.html``:

.. literalinclude:: ../../test_project/template_autocomplete/templates/template_autocomplete/templated_choice.html
   :language: django

Alternative
-----------

FTR, here's another way to do it, assuming your models have a
`get_absolute_update_url` method defined::

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
