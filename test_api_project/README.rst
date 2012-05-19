This project demonstrates how the autocomplete can suggest results from a
remote API - and thus which don't have a pk in the local database.

In one console::
    
    cd test_project
    ./manage.py runserver

In another::

    cd test_api_project
    ./manage.py runserver 127.0.0.1:8001

Now, note that there are `no or few countries in test_api_project database
<http://localhost:8001/admin/cities_light/country/>`_.

Also note that, city and country autocomplete `work the same
<http://localhost:8001/admin/project_specific/contact/add/>`_. The reason for
that is that test_api_project uses City and Country remote channel to add
results to the autocomplete that are not in the local database.
