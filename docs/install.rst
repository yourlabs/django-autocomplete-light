Install django-autocomplete-light v3
====================================

Install version 3 with :pip:ref:`pip install`::

    pip install -e git+https://github.com/yourlabs/django-autocomplete-light.git@v3#egg=dal

Then, let Django find static file we need by adding to
:django:setting:`INSTALLED_APPS`::

    'dal',
    'dal_select2',
