Install django-autocomplete-light v3
====================================

Install in your project
-----------------------

Install version 3 with :pip:ref:`pip install`::

    pip install django-autocomplete-light

Or, install the dev version with git::

    pip install -e git+https://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light

.. note::
   If you are trying to install from git, please make sure you are not using
   **zip/archive** url of the repo ``django-autocomplete-light`` since it will not
   contain required submodules automatically. Otherwise these submodules will then
   need to be updated separately using ``git submodule update --init``.

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

Django versions earlier than 2.0
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You will need to add dal_legacy_static to your INSTALLED_APPS settings.
This adds in select2 static files that are included with Django 2.x but
missing in earlier versions.

JQuery 3.x
^^^^^^^^^^
JQuery 3.x comes with a "slim" version. This "slim" version is not compatible with
DAL since the slim version does not contain Ajax functionality.

.. _demo-install:

Install the demo project
------------------------

Install the demo project in a temporary virtualenv for testing purpose::

    cd /tmp
    virtualenv -p python3 dal_env
    source dal_env/bin/activate
    pip install django
    pip install -e git+https://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light
    cd dal_env/src/django-autocomplete-light/test_project/
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver
    # go to http://localhost:8000/admin/ and login
