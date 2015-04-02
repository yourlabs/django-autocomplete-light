test_project: basic features and examples
=========================================

Virtualenv is a great solution to isolate python environments. If necessary,
you can install it from your package manager or the python package manager,
ie.::

    sudo easy_install virtualenv

Install last release
--------------------

Install packages from PyPi and the test project from Github::

    rm -rf django-autocomplete-light autocomplete_light_env/

    virtualenv autocomplete_light_env
    source autocomplete_light_env/bin/activate
    git clone https://jpic@github.com/yourlabs/django-autocomplete-light.git
    cd django-autocomplete-light/test_project
    pip install -r requirements.txt
    ./manage.py runserver

Or install the development version
----------------------------------

Install directly from github::

    rm -rf autocomplete_light_env/

    virtualenv autocomplete_light_env
    source autocomplete_light_env/bin/activate
    pip install -e git+git://github.com/yourlabs/django-autocomplete-light.git#egg=autocomplete_light
    cd autocomplete_light_env/src/autocomplete-light/test_project
    pip install -r requirements.txt
    ./manage.py runserver

Usage
-----

- Run the server,
- Connect to `/admin/`, ie. http://localhost:8000/admin/,
- Login with user "test" and password "test",
- Try the many example applications,

Database
--------

A working SQLite database is shipped, but you can make your own ie.::

    cd test_project
    rm -rf db.sqlite
    ./manage.py syncdb --noinput
    ./manage.py migrate
    ./manage.py cities_light

Note that `test_project/project_specific/models.py` filters cities from certain
countries.
