This commands should run the test project server::

    AUTOCOMPLETE_LIGHT_VERSION="test_project"
    CITIES_LIGHT_VERSION="test_project"

    virtualenv autocomplete_light_env
    source autocomplete_light_env/bin/activate
    pip install -e git+git://github.com/yourlabs/django-cities-light.git@$CITIES_LIGHT_VERSION#egg=cities_light
    pip install -e git+git://github.com/yourlabs/django-autocomplete-light.git@$AUTOCOMPLETE_LIGHT_VERSION#egg=autocomplete_light
    cd autocomplete_light_env/src/autocomplete-light/test_project
    pip install -r requirements.txt
    ./manage.py runserver

If you want to redo the database, but make sure you read README first::

    rm db.sqlite
    ./manage.py syncdb
    ./manage.py cities_light
