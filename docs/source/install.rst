Install the package with pip
----------------------------

Install the stable release::

    pip install django-autocomplete-light

Or the development version::

    pip install -e git+https://github.com/yourlabs/django-autocomplete-light#egg=autocomplete_light

Append ``'autocomplete_light'`` to ``settings.INSTALLED_APPS``
--------------------------------------------------------------

Enable templates and static files by adding ``autocomplete_light`` to
``settings.INSTALLED_APPS``, it can look like this:

  .. code-block:: python

    INSTALLED_APPS = [
        # [...] your list of app packages is here, add this:
        'autocomplete_light',
    ]

Call ``autocomplete_light.autodiscover()`` *before* ``admin.autodiscover()``
----------------------------------------------------------------------------

In ``urls.py``, call ``autocomplete_light.autodiscover()`` before
``admin.autodiscover()``, it can look like this:

  .. code-block:: python

    import autocomplete_light
    # import every app/autocomplete_light_registry.py
    autocomplete_light.autodiscover()

    import admin
    admin.autodiscover()

Include ``autocomplete_light.urls``
-----------------------------------

Install the autocomplete view and staff debug view in ``urls.py`` it can look
like this:

  .. code-block:: python

    urlpatterns = patterns('',
        # [...] your url patterns are here
        url(r'^autocomplete/', include('autocomplete_light.urls')),
    )

Ensure understanding of ``django.contrib.staticfiles``
------------------------------------------------------

Ensure that you understand django-staticfiles, if you don't try this article.

Include ``autocomplete_light/static.html`` after loading jquery.js
------------------------------------------------------------------

Load the javascript scripts after loading ``jquery.js``, it can look like this:

  .. code-block:: django

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.js" type="text/javascript"></script>
    {% include 'autocomplete_light/static.html' %}

Optionnaly include it in ``admin/base_site.html`` too
-----------------------------------------------------

For admin support, install it in ``admin/base_site.html``, it could look like
this:

  .. code-block:: django

    {% extends "admin/base.html" %}

    {% block extrahead %}
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.js" type="text/javascript"></script>
        {% include 'autocomplete_light/static.html' %}
    {% endblock %}

.. note::

    There is **nothing** magic in how the javascript loads. This means that you can
    use ``django-compressor`` or anything.

.. info::

    Also, why are we not using ``Widget.Media`` ? See FAQ.
