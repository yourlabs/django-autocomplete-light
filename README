.. image:: https://img.shields.io/pypi/dm/django-autocomplete-light.svg
   :target: https://pypi.python.org/pypi/django-autocomplete-light
.. image:: https://badge.fury.io/py/django-autocomplete-light.png
   :target: http://badge.fury.io/py/django-autocomplete-light
.. image:: https://secure.travis-ci.org/yourlabs/django-autocomplete-light.png?branch=master
    :target: http://travis-ci.org/yourlabs/django-autocomplete-light
.. image:: https://codecov.io/github/yourlabs/django-autocomplete-light/coverage.svg?branch=master
    :target: https://codecov.io/github/yourlabs/django-autocomplete-light?branch=master

django-autocomplete-light's purpose is to enable autocompletes quickly and
properly in a django project: it is the fruit of half a decade of R&D and
thousands of contributions. It was designed for Django so that every part
overridable or reusable independently. It is stable, tested, documented and
fully supported: it tries to be a good neighbour in Django ecosystem.

Projects upgrading to Django 1.9
--------------------------------

DAL has been ready for Django 1.9 since April 2015 thanks to @blueyed & @jpic.
**HOWEVER** due to the app loading refactor in 1.9 you should apply the
following::

    find . -name '*.py' | xargs perl -i -pe 's/import autocomplete_light/from autocomplete_light import shortcuts as autocomplete_light/'

See the test_project running on Django 1.9 and its new cool admin theme:
http://dal-yourlabs.rhcloud.com/admin (test:test).

Features
--------

Features include:

- charfield, foreign key, many to many autocomplete widgets,
- generic foreign key, generic many to many autocomplete widgets,
- django template engine support for autocompletes, enabling you to include
  images etc ...
- 100% overridable HTML, CSS, Python and Javascript: there is no variable
  hidden far down in the scope anywhere.
- add-another popup supported outside the admin too.
- keyboard is supported with enter, tab and arrows by default.
- Django 1.7 to 1.10, PyPy, Python 2 and 3, PostgreSQL, SQLite, MySQL

Each feature has a live example and is fully documented. It is also designed
and documented so that you create your own awesome features too.

Resources
---------

Resources include:

- `**Documentation** graciously hosted
  <http://django-autocomplete-light.rtfd.org>`_ by `RTFD
  <http://rtfd.org>`_
- `Live demo graciously hosted
  <http://dal-yourlabs.rhcloud.com/>`_ by `RedHat
  <http://openshift.com>`_, thanks to `PythonAnywhere
  <http://pythonanywhere.com/>`_ for hosting it in the past,
- `Video demo graciously hosted
  <http://youtu.be/fJIHiqWKUXI>`_ by `Youtube
  <http://youtube.com>`_,
- `Mailing list graciously hosted
  <http://groups.google.com/group/yourlabs>`_ by `Google
  <http://groups.google.com>`_
- `Git graciously hosted
  <https://github.com/yourlabs/django-autocomplete-light/>`_ by `GitHub
  <http://github.com>`_,
- `Package graciously hosted
  <http://pypi.python.org/pypi/django-autocomplete-light/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_,
- `Continuous integration graciously hosted
  <http://travis-ci.org/yourlabs/django-autocomplete-light>`_ by `Travis-ci
  <http://travis-ci.org>`_
- `**Online paid support** provided via HackHands
  <https://hackhands.com/jpic/>`_,
