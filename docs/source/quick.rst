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

.. include:: _admin_template.rst

Create yourapp/autocomplete_light_registry.py, assuming "Author" has a "name" CharField::

    import autocomplete_light

    from models import Author

    autocomplete_light.register(Author)

See more about the channel registry in :ref:`registry-reference`.

If Author doesn't has another CharField, like full_name, then you could change
the name of the search field::

    import autocomplete_light

    from models import Author

    class AuthorChannel(autocomplete_light.ChannelBase):
        search_field = 'full_name'

    # register Author with AuthorChannel !
    autocomplete_light.register(Author, AuthorChannel)

But still, the `default implementation of query_filter()
<forms.html#autocomplete_light.channel.base.ChannelBase.get_results>`_ is
pretty trivial, you might want to customize how it will filter the queryset::

    from django.db.models import Q

    import autocomplete_light

    from models import Author

    class AuthorChannel(autocomplete_light.ChannelBase):
        def query_filter(self, results):
            q = self.request.GET.get('q', None)

            if q:
                results = results.filter(
                    Q(first_name__icontains=q)|Q(last_name__icontains=q))

            return results

    autocomplete_light.register(Author, AuthorChannel)

See more about customizing channels in :ref:`channel-reference`.

Finnaly in yourapp/admin.py::

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
