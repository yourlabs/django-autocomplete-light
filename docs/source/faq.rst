Why not use Widget.Media ?
--------------------------

In the early versions (0.1) of django-autocomplete-light, we had widgets
defining the Media class like this:

.. code-block:: python

    class AutocompleteWidget(forms.SelectMultiple):
        class Media:
            js = ('autocomplete_light/autocomplete.js',)


This caused a problem if you want to load jquery and autocomplete.js globally
**anyway** and **anywhere** in the admin to have a global navigation
autocomplete: it would double load the scripts.

Also, this didn't work well with django-compressor and other cool ways of
deploying the JS.

So, in the next version, I added a dependency management system. Which sucked
and was removed right away to finally keep it simple and stupid as we have it
today.

Model field's ``help_text`` and ``verbose_name`` are lost when overriding the widget
------------------------------------------------------------------------------------

This has nothing to do with django-autocomplete-light, but still it's a FAQ so
here goes.

When Django's ModelForm creates a form field for a model field, it copies
:py:attr:`models.Field.verbose_name
<django:django.db.models.Field.verbose_name>` to :py:attr:`forms.Field.label
<django:django.forms.Field.label>` and :py:attr:`models.Field.help_text
<django:django.db.models.Field.help_text>` to :py:attr:`forms.Field.help_text
<django:django.forms.Field.help_text>`, as uses  :py:attr:`models.Field.blank
<django:django.db.models.Field.blank>` to create :py:attr:`forms.Field.required
<django:django.forms.Field.required>`.

For example:

.. code-block:: python

    class Person(models.Model):
        name = models.CharField(
            max_length=100, 
            blank=True,
            verbose_name='Person name', 
            help_text='Please fill in the complete person name'
        )

    class PersonForm(forms.ModelForm):
        class Meta:
            model = Person

Thanks to Django's DRY system, this is equivalent to:

.. code-block:: python

    class PersonForm(forms.ModelForm):
        name = forms.CharField(
            max_length=100,
            required=False,
            label='Person name',
            help_text='Please fill in the complete person name'
        )

        class Meta:
            model = Person

But you will loose that logic as soon as you decide to override Django's
generated form field with your own. So if you do this:

.. code-block:: python

    class PersonForm(forms.ModelForm):
        name = forms.CharField(widget=YourWidget)

        class Meta:
            model = Person

Then you loose Django's DRY system, because **you** instanciate the name form
field, so Django leaves it as is.

If you want to override the widget of a form field and you **don't** want to
override the form field, then you should refer to `Django's documentation on
overriding the default fields
<http://docs.djangoproject.com/topics/forms/modelforms.html#overriding-the-default-fields>`_
which means you should use ``Meta.widgets``, ie.:

.. code-block:: python

    class PersonForm(forms.ModelForm):
        class Meta:
            model = Person
            widgets = {'name': YourWidget}

Again, this has nothing to do with django-autocomplete-light.

How to override a JS method ?
-----------------------------



How to work around Django bug #9321: `Hold down "Control" ...` ?
----------------------------------------------------------------

How to report a bug effectively ?
---------------------------------

Read `How to Report Bugs Effectively
<http://www.chiark.greenend.org.uk/~sgtatham/bugs.html>`_ and open an issue on
`django-autocomplete-light's issue tracker on GitHub
<https://github.com/yourlabs/django-autocomplete-light/issues>`_.

How to ask for help ?
---------------------

The best way to ask for help is:

- fork the repo,
- add a simple way to reproduce your problem in a new app of test_project, try
  to keep it minimal,
- open an issue on github and mention your fork.

Really, it takes quite some time for me to clean pasted code and put up an
example app it would be really cool if you could help me with that !

If you don't want to do the fork and the reproduce case, then you should better
ask on StackOverflow and you might be lucky (just tag your question with
django-autocomplete-light to ensure that I find it).
