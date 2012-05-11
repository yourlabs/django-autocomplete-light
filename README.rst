This is a simple alternative to django-ajax-selects.

Resources
---------

Documentation graciously hosted by RTFD:
http://django-autocomplete-light.rtfd.org

Continuous integration graciously hosted by Travis:
http://travis-ci.org/yourlabs/django-autocomplete-light

Git graciously hosted by GitHub:
https://github.com/yourlabs/django-autocomplete-light/

Demo
----

Just open http://127.0.0.1:8000/admin (user: test, pass: test) after doing::

    virtualenv autocomplete_light_env
    source autocomplete_light_env/bin/activate
    pip install -e git+git://github.com/yourlabs/django-autocomplete-light.git#egg=autocomplete_light
    cd autocomplete_light_env/src/autocomplete_light/test_project
    ./manage.py runserver

Now, open this contact: http://localhost:8000/admin/project_specific/contact/1/
You will note two addresses:

- one at Paris, France
- one at Paris, United States

The reason for that is that there are several cities in the world with the name
"Paris". This is the reason why the double autocomplete widget is interresting:
it filters the cities based on the selected country.

Note that only cities from France, USA and Belgium are in the demo database.

If you want to redo the database::

    rm db.sqlite
    ./manage.py syncdb
    ./manage.py cities_light
