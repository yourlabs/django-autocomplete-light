Install django-autocomplete-light v3
====================================

Install in your project
-----------------------

Install version 3 with :pip:ref:`pip install`::

    pip install django-autocomplete-light

Or, install the dev version with git::

    pip install -e git+https://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light

Then, let Django find static file we need by adding to
:django:setting:`INSTALLED_APPS`, **before** ``django.contrib.admin``::

    'dal',
    'dal_select2',
    'django.contrib.admin',

This is to override the ``jquery.init.js`` script provided by the admin, which
sets up jQuery with ``noConflict``, making jQuery available in
``django.jQuery`` only and not ``$``.

Install the demo project
------------------------

Install the demo project in a temporary virtualenv for testing purpose::

    cd /tmp
    virtualenv dal_env
    source dal_env/bin/activate
    pip install django
    pip install -e git+https://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light
    cd dal_env/src/django-autocomplete-light/test_project/
    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver
    # go to http://localhost:8000/admin/ and login
