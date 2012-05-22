Install last release::

    rm -rf django-autocomplete-light autocomplete_light_env/

    virtualenv autocomplete_light_env
    source autocomplete_light_env/bin/activate
    git clone https://jpic@github.com/yourlabs/django-autocomplete-light.git
    cd django-autocomplete-light/test_project
    pip install -r requirements.txt
    ./manage.py runserver

Install development versions, if you want to contribute hehehe::

    AUTOCOMPLETE_LIGHT_VERSION="master"
    CITIES_LIGHT_VERSION="master"

    rm -rf autocomplete_light_env/

    virtualenv autocomplete_light_env
    source autocomplete_light_env/bin/activate
    pip install -e git+git://github.com/yourlabs/django-cities-light.git@$CITIES_LIGHT_VERSION#egg=cities_light
    pip install -e git+git://github.com/yourlabs/django-autocomplete-light.git@$AUTOCOMPLETE_LIGHT_VERSION#egg=autocomplete_light
    cd autocomplete_light_env/src/autocomplete-light/test_project
    pip install -r requirements.txt
    ./manage.py runserver

Login with user "test" and password "test".

If you want to redo the database, but make sure you read README first::

    rm db.sqlite
    ./manage.py syncdb
    ./manage.py cities_light
