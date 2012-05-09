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

Here's the list of scripts you might need:

- autocomplete_light/autocomplete.js: for any kind of autocomplete
- autocomplete_light/deck.js: for autocomplete form fields

Also, each app might provide its own channel and bootstrap javascripts. They
should be in app/static/appname/autocomplete_light.js. For example, cities_list
has cities_light/static/cities_light/autocomplete_light.js.

For your convenience, those are autodiscovered. To load all these scripts::

    {% load autocomplete_light_tags %}
    {% autocomplete_light_js %}

Note that this will also generate script tags for autocomplete.js and deck.js by default.

Obviously, you should put this after your script tag that loads jQuery.

Also, remember that deck.js is only required by AutocompleteWidget. If
you only intend to make a global navigation autocomplete then you just
need autocomplete.js::

    <script src="{{ STATIC_URL }}autocomplete_light/autocomplete.js" type="text/javascript"></script>
