Quick start
===========

The purpose of this documentation is to get you started as fast as possible,
because your time matters and you probably have other things to worry about.

Quick install
-------------

Install the package::

    pip install django-autocomplete-light
    # or the development version
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

Quick form integration
----------------------

AutocompleteWidget is usable on ModelChoiceField and ModelMultipleChoiceField.

.. autoclass:: autocomplete_light.widgets.AutocompleteWidget
   :noindex:
