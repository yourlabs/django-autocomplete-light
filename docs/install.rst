Install
=======

In your project
---------------

Install with ``pip``::

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
Add ``dal`` and ``dal_alight`` to ``INSTALLED_APPS`` **before**
``django.contrib.admin`` (and ``grappelli`` if present) so that DAL can
override admin widget templates::

    'dal',
    'dal_alight',
    # 'grappelli',
    'django.contrib.admin',

To enable more DAL functionalities we will have to add other DAL apps
to ``INSTALLED_APPS``, such as ``'dal_queryset_sequence'`` ...

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
