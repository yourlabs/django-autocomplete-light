Quick start
===========

The purpose of this documentation is to get you started as fast as possible,
because your time matters and you probably have other things to worry about.

Quick install
-------------

Install the package::

    pip install django-autocomplete-light
    # or the development version
    pip install -e git+git://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light

Add to INSTALLED_APPS: 'autocomplete_light'

Add to urls::

    url(r'autocomplete/', include('autocomplete_light.urls')),

Add before admin.autodiscover() and **any form import** for that matter::

    import autocomplete_light
    autocomplete_light.autodiscover()

At this point, we're going to assume that you have `django.contrib.staticfiles
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>`_ working.
This means that `static files are automatically served with runserver
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#runserver>`_,
and that you have to run `collectstatic when using another server
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#collectstatic>`_
(fastcgi, uwsgi, and whatnot). If you don't use django.contrib.staticfiles,
then you're on your own to manage staticfiles.

.. _javascript-setup:

This is an example of how you could load the javascript::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
    {% include 'autocomplete_light/static.html' %}

Note that you should adapt the static.html template to your needs at some
point, because its purpose is to work for all projects, not to be optimal for
your project.

.. _quick-admin:

Quick admin integration
-----------------------

.. include:: _admin_template.rst

Create ``yourapp/autocomplete_light_registry.py``, you can copy this example autocomplete :ref:`registry-reference`:

.. literalinclude:: ../../test_project/fk_autocomplete/autocomplete_light_registry.py
   :language: python

At this point, the easiest is to use autocomplete-light's modelform_factory
shortcut directly in ``yourapp/admin.py``, ie.:

.. literalinclude:: ../../test_project/fk_autocomplete/admin.py
   :language: python

Quick form integration
----------------------

Example models:

.. literalinclude:: ../../test_project/non_admin/models.py
   :language: python

Example forms:

.. literalinclude:: ../../test_project/non_admin/forms.py
   :language: python

Example urls:

.. literalinclude:: ../../test_project/non_admin/urls.py
   :language: python

.. Note::
    It is not mandatory to use url namespaces.

Example template:

.. literalinclude:: ../../test_project/non_admin/templates/non_admin/widget_form.html
   :language: django

You can manually use autocomplete_light.ChoiceWidget or
autocomplete_light.MultipleChoiceWidget for django's ModelChoiceField and
ModelMultipleChoiceField respectively.

.. automodule:: autocomplete_light.widgets
   :noindex:
