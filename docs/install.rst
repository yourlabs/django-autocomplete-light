Install
=======

In your project
---------------

Install version 3 with :pip:ref:`pip install`::

    pip install django-autocomplete-light

Or, install the dev version with git::

    pip install -e git+https://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light

Optional dependencies
^^^^^^^^^^^^^^^^^^^^^

Install extras as needed::

    pip install django-autocomplete-light[gfk]     # GenericForeignKey support (django-querysetsequence)
    pip install django-autocomplete-light[tags]    # django-taggit support
    pip install django-autocomplete-light[nested]  # django-nested-admin support

Configuration
-------------
Then, to let Django find the static files we need by adding to
:django:setting:`INSTALLED_APPS`, **before** ``django.contrib.admin`` and
``grappelli`` if present::

    'dal',
    'dal_select2',
    # 'grappelli',
    'django.contrib.admin',

This is to override the ``jquery.init.js`` script provided by the admin, which
sets up jQuery with ``noConflict``, making jQuery available in
``django.jQuery`` only and not ``$``.

To enable more DAL functionalities we will have to add other DAL apps
to :django:setting:`INSTALLED_APPS`, such as 'dal_queryset_sequence' ...

JQuery 3.x
^^^^^^^^^^
JQuery 3.x comes with a "slim" version. This "slim" version is not compatible with
DAL since the slim version does not contain Ajax functionality.

.. _demo-install:

Install the demo project
------------------------

Install the demo project in a temporary virtualenv for testing purpose::

    cd /tmp
    python3 -m venv dal_env
    source dal_env/bin/activate
    pip install -e git+https://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light
    cd dal_env/src/django-autocomplete-light/test_project/
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver
    # go to http://localhost:8000/admin/ and login
