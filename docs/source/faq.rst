How to run tests
----------------

You should not try to ``test autocomplete_light`` from your own project because
tests depend on example apps to be present in ``INSTALLED_APPS``. You may use
the provided ``test_project`` which is prepared to run all testst.

Install a version from git, ie::

    pip install -e git+https://github.com/yourlabs/django-autocomplete-light.git#egg=autocomplete_light

From there you have two choices:

- either go in ``env/src/autocomplete_light/test_project`` and run
  ``./manage.py test autocomplete_light``,
- either go in ``env/src/autocomplete_light/`` and run ``tox`` after installing
  it from pip.

If you're trying to run a buildbot then you can use ``test.sh`` and use that
buildbot configuration to enable CI on the 28 supported configurations:

.. code-block:: python

    def make_build(python, django, genericm2m, taggit):
        name = 'py%s-dj%s' % (python, django)
    
        if genericm2m != '0':
            name += '-genericm2m'
        if taggit != '0':
            name += '-taggit'
    
        slavenames = ['example-slave']
        if python == '2.7':
            slavenames.append('gina')
    
        factory = BuildFactory()
        # check out the source
        factory.addStep(Git(repourl='https://github.com/yourlabs/django-autocomplete-light.git', mode='incremental'))
        # run the tests (note that this will require that 'trial' is installed)
        factory.addStep(ShellCommand(command=["./test.sh"], timeout=3600))
    
        c['builders'].append(
            BuilderConfig(name=name,
                slavenames=slavenames,
                factory=factory,
                env={
                    'DJANGO_VERSION': django,
                    'PYTHON_VERSION': python,
                    'DJANGO_GENERIC_M2M': genericm2m,
                    'DJANGO_TAGGIT': taggit,
                }
            )
        )
    
        c['schedulers'].append(SingleBranchScheduler(
                            name="all-%s" % name,
                            change_filter=filter.ChangeFilter(branch='v2'),
                            treeStableTimer=None,
                            builderNames=[name]))
        c['schedulers'].append(ForceScheduler(
                            name="force-%s" % name,
                            builderNames=[name]))
    
    
    c['builders'] = []
    djangos = ['1.4', '1.5', '1.6']
    pythons = ['2.7', '3.3']
    
    for python in pythons:
        for django in djangos:
            if python == '3.3' and django == '1.4':
                continue
    
            for genericm2m in ['0','1']:
                for taggit in ['0','1']:
                    make_build(python, django, genericm2m, taggit)
    
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

.. _dry-break:

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

Fields bound on values which are not in the queryset anymore raise a ValidationError
------------------------------------------------------------------------------------

This is not specific to django-autocomplete-light, but still it's a FAQ so here
goes.

Django **specifies in its unit tests** that a ``ModelChoiceField`` and
``ModelMultipleChoiceField`` should raise a ``ValidationError`` if a value is
not part of the ``queryset`` passed to the field constructor.

This is the `relevant part of Django's specification
<https://github.com/django/django/blob/16d73d7416a7902703ee8022f093667f7ac9ef5b/tests/model_forms/tests.py#L1251>`_:

.. code-block:: python

        # Delete a Category object *after* the ModelChoiceField has already been
        # instantiated. This proves clean() checks the database during clean() rather
        # than caching it at time of instantiation.
        Category.objects.get(url='5th').delete()
        with self.assertRaises(ValidationError):
            f.clean(c5.id)

        # [...]

        # Delete a Category object *after* the ModelMultipleChoiceField has already been
        # instantiated. This proves clean() checks the database during clean() rather
        # than caching it at time of instantiation.
        Category.objects.get(url='6th').delete()
        with self.assertRaises(ValidationError):
            f.clean([c6.id])

django-autocomplete-light behaves exactly the same way. If an item is removed
from the queryset, then its value will be dropped from the field values on
display of the form. Trying to save that value again will raise a
ValidationError will be raised, just like if the item wasn't there at all.

But don't take my word for it, try the ``security_test`` app of the
``test_project``, it provides:

- an admin to control which items are in and out of the queryset,
- an update view with a django select
- another update view with an autocomplete instead

How to override a JS method ?
-----------------------------

Refer to :ref:`script-method-override`.

How to work around Django bug #9321: `Hold down "Control" ...` ?
----------------------------------------------------------------

Just use the :py:class:`autocomplete_light.ModelForm
<autocomplete_light.forms.ModelForm>` or inherit from both
:py:class:`~autocomplete_light.forms.SelectMultipleHelpTextRemovalMixin`
and :py:class:`django.forms.ModelForm`.

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
