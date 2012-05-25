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

At this point, we're going to assume that you have `django.contrib.staticfiles
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>`_ working.
This means that `static files are automatically served with runserver
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#runserver>`_,
and that you have to run `collectstatic when using another server
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#collectstatic>`_
(fastcgi, uwsgi, and whatnot). If you don't use django.contrib.staticfiles,
then you're on your own to manage staticfiles.

.. _javascript-setup:

This is an example of how you could load the javascript::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>
    {% include 'autocomplete_light/static.html' %}

.. _quick-admin:

Quick admin integration
-----------------------

.. include:: _admin_template.rst

Create yourapp/autocomplete_light_registry.py, assuming "Author" has a "full_name" CharField::

    import autocomplete_light

    from models import Author

    autocomplete_light.register(Author, search_field='full_name')

See more about the channel registry in :ref:`registry-reference`.

But still, the `default implementation of query_filter()
<forms.html#autocomplete_light.channel.base.ChannelBase.query_filter>`_ is
pretty trivial, you might want to customize how it will filter the queryset.
See more about customizing channels in :ref:`channel-reference`.

Anyway, finish by setting ``BookAdmin.form`` in yourapp/admin.py::

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
