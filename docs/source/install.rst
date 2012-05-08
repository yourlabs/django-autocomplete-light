Installing django-autocomplete-light
====================================

The installation procedure is pretty much the same than for any django
app. The procedure is described here as a reference.

Install the package
-------------------

Install the stable package (not yet released)::

    pip install django-autocomplete-light

Or, install the development version::

    pip install -e git+git://github.com/yourlabs/django-autocomplete-light.git#egg=django-autocomplete-light

Install the app
---------------

If you want Django to get the static files directly from the package,
then add the app to INSTALLED_APPS, in settings.py::

    INSTALLED_APPS = (
        # ... your app list
        'autocomplete_light',
    )

Install the urls
----------------

In your urls module, probably urls.py, you can add something like
this::

    urlpatterns = patterns('',
        # ... your url list
        url(r'autocomplete/', include('autocomplete_light.urls')),
    )

Install the javascript
----------------------

Load jQuery
~~~~~~~~~~~

You could load jQuery with something like this::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript"></script>

Note that it was developed with jQuery 1.7.1.

Load the scripts
~~~~~~~~~~~~~~~~

If you're using
`django.contrib.staticfiles<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>_`
or Pinax, this would work::
    
    <script src="{{ STATIC_URL }}autocomplete_light/autocomplete.js" type="text/javascript"></script>
    <script src="{{ STATIC_URL }}autocomplete_light/deck.js" type="text/javascript"></script>

Obviously, you should put this after your script tag that loads jQuery.

Also, remember that deck.js is only required by AutocompleteWidget. If
you only intend to make a global navigation autocomplete then you just
need autocomplete.js.
