Once you have the test_project server running (see INSTALL if you don't), open
`the first contact
<http://localhost:8000/admin/project_specific/contact/1/>`_.

You will see two addresses:

- one at Paris, France
- one at Paris, United States

The reason for that is that there are several cities in the world with the name
"Paris". This is the reason why the double autocomplete widget is interresting:
it filters the cities based on the selected country.

Note that only cities from France, USA and Belgium are in the demo database.
