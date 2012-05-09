Welcome to django-autocomplete-light's documentation!
=====================================================

Features
--------

This app fills all your ajax autocomplete needs:

- global navigation autocomplete like on http://betspire.com
- autocomplete widget for ModelChoiceField and ModelMultipleChoiceField
- **0 hack** required for admin integration, just use a form that uses the
  widget
- **no jQuery-ui** required, the autocomplete script is as simple as possible
- **all** the design of the autocompletes is encapsulated in template,
  unlimited design possibilities
- **99%** of the python logic is encapsulated in "channel" classes, unlimited
  development possibilities
- **99%** the javascript logic is encapsulated in an "options" array, 
  unlimited development possibilities
- **no** inline javascript, you can load the javascript just before </body> for
  best page loading performance
- **simple** python, html and javascript, easy to hack
- **less sucking** code, no funny hacks, clean api, as few code as
  possible, that also means this is not for pushovers

Quick install
-------------


Install the package::

    pip install -e git+git://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light

Add to INSTALLED_APPS: 'autocomplete_light'

Add to urls::

    url(r'autocomplete/', include('autocomplete_light.urls')),

Add before admin.autodiscover()::

    import autocomplete_light
    autocomplete_light.autodiscover()

Add to your base template::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
    {% load autocomplete_light_tags %}
    {% autocomplete_light_static %}

Quick admin integration
-----------------------

Create yourapp/autocomplete_light_registry.py::

    import autocomplete_light

    from models import Author

    autocomplete_light.register(Author)

In yourapp/admin.py::

    from django.contrib import admin

    import autocomplete_light

    from models import Book

    class BookAdmin(admin.ModelAdmin):
        # use an autocomplete for Author
        form = autocomplete_light.modelform_factory(Book)
    admin.site.register(Book, BookAdmin)

Full documentation
------------------

.. toctree::
   :maxdepth: 2

   design
   install
   navigation
   forms
   templating
   admin
   funny

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

