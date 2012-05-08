Autocompletes in admin
======================

You're probably on a hurry so I'm not going to waste your time. This chapter is
minimal, refer to other chapters for details.

Say you want an autocomplete for the 'author' field of the Book form.

In urls.py::

    # put this BEFORE admin.autodiscover()
    import autocomplete_light
    autocomplete_light.autodiscover()

In yourapp/autocomplete_light_registry.py::

    import autocomplete_light

    from models import Author

    autocomplete_light.register(Author)

In yourapp/admin.py::

    from django.contrib import admin

    import autocomplete_light

    from models import Book

    class BookAdmin(admin.ModelAdmin):
        form = autocomplete_light.modelform_factory(Book)
    admin.site.register(Book, BookAdmin)

Assuming you've installed the javascript right, that's all you have to do.
