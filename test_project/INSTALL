This commands should run the test project server::

    virtualenv autocomplete_light_env
    source autocomplete_light_env/bin/activate
    pip install -e git+git://github.com/yourlabs/django-autocomplete-light.git@test_project#egg=autocomplete_light
    cd autocomplete_light_env/src/autocomplete-light/test_project
    pip install -r requirements.txt
    ./manage.py runserver

If you want to redo the database, but make sure you read README first::

    rm db.sqlite
    ./manage.py syncdb
    ./manage.py cities_light
