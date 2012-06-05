This project demonstrates how the autocomplete can suggest results from a
remote API - and thus which don't have a pk in the local database.

In one console::

    cd test_project
    ./manage.py runserver

In another::

    cd test_api_project
    ./manage.py runserver 127.0.0.1:8001

In http://localhost:8001/admin, you should be able to test:

- compatibility with django-admintools-bootstrap
- generic fk autocomplete
- generic m2m autocomplete
- remote api autocomplete (cities/countries are suggested and imported from
  test_project)
- autocompletes in inlines, dual widget, etc, etc ...

If you're not going to use localhost:8000 for test_project, then you should
update source urls in
`test_api_project/test_api_project/autocomplete_light_registry.py`.

Now, note that there are `no or few countries in test_api_project database
<http://localhost:8001/admin/cities_light/country/>`_.

Again, test_project's database only includes countries France, Belgium and
America so there's no need to try the other one unless you know what you're
doing.

Also note that, city and country autocomplete `work the same
<http://localhost:8001/admin/project_specific/contact/add/>`_. The reason for
that is that test_api_project uses City and Country remote channel to add
results to the autocomplete that are not in the local database.
