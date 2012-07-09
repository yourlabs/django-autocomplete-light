test_remote_project: advanced features and examples
===================================================

The autocomplete can suggest results from a remote API - objects that do not
exist in the local database.

This project demonstrates how test_remote_project can provide autocomplete
suggestions using the database from test_project.

Usage
-----

In one console::

    cd test_project
    ./manage.py runserver

In another::

    cd test_remote_project
    ./manage.py runserver 127.0.0.1:8001

Now, note that there are `no or few countries in test_api_project database
<http://localhost:8001/admin/cities_light/country/>`_.

Then, connect to http://localhost:8001/admin/remote_autocomplete/address/add/
and the city autocomplete should propose cities from both projects.

If you're not going to use localhost:8000 for test_project, then you should
update source urls in
`test_remote_project/remote_autocomplete/autocomplete_light_registry.py`.
