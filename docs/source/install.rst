Install the ``django-autocomplete-light`` package with pip
----------------------------------------------------------

Install the stable release, preferably in a `virtualenv
<http://virtualenv.org>`_::

    pip install django-autocomplete-light

Or the development version::

    pip install -e git+https://github.com/yourlabs/django-autocomplete-light#egg=autocomplete_light

Append ``'autocomplete_light'`` to ``settings.INSTALLED_APPS``
--------------------------------------------------------------

Enable templates and static files by adding ``autocomplete_light`` to
`settings.INSTALLED_APPS
<https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps>`_ which is
editable in ``settings.py``, it can look like this:

.. code-block:: python

    INSTALLED_APPS = [
        # [...] your list of app packages is here, add this:
        'autocomplete_light',
    ]

Call ``autocomplete_light.autodiscover()`` *before* ``admin.autodiscover()``
----------------------------------------------------------------------------

In ``urls.py``, call ``autocomplete_light.autodiscover()`` before
``admin.autodiscover()`` **and before any import of a form with
autocompletes**, it can look like this:

.. code-block:: python

    import autocomplete_light
    # import every app/autocomplete_light_registry.py
    autocomplete_light.autodiscover()

    import admin
    admin.autodiscover()

Also, if you have ``yourapp.views`` which imports a form that has autocomplete,
say ``SomeForm``, this would work:

.. code-block:: python

    import autocomplete_light
    autocomplete_light.autodiscover()

    from yourapp.views import SomeCreateView

But that wouldn't:

.. code-block:: python

    from yourapp.views import SomeCreateView

    import autocomplete_light
    autocomplete_light.autodiscover()

That is because auto-discovery of autocomplete classes should happen before
definition of forms using autocompletes.

Include ``autocomplete_light.urls``
-----------------------------------

Install the autocomplete view and staff debug view in ``urls.py``
using the `include function
<https://docs.djangoproject.com/en/dev/topics/http/urls/#including-other-urlconfs>`_,
it can look like this:

.. code-block:: python

    # Django 1.5:
    from django.conf.urls import patterns, url, include

    # In Django 1.4:
    # from django.conf.urls.default import patterns, url, include

    urlpatterns = patterns('',
        # [...] your url patterns are here
        url(r'^autocomplete/', include('autocomplete_light.urls')),
    )

Ensure understanding of ``django.contrib.staticfiles``
------------------------------------------------------

Ensure that you understand django-staticfiles, if you don't try `this
article
<http://blog.yourlabs.org/post/30382323418/surviving-django-contrib-staticfiles-or-how-to-manage>`_ 
or refer to official `howto
<https://docs.djangoproject.com/en/dev/howto/static-files/>`_ and `topic
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>`_.

Include ``autocomplete_light/static.html`` after loading jquery.js (>=1.7)
--------------------------------------------------------------------------

Load the javascript scripts after loading ``jquery.js``, it can look like this:

.. code-block:: django

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.js" type="text/javascript"></script>
    {% include 'autocomplete_light/static.html' %}

Optionaly include it in ``admin/base_site.html`` too
-----------------------------------------------------

For admin support, `override
<http://blog.yourlabs.org/post/19777151073/how-to-override-a-view-from-an-external-django-app>`_
``admin/base_site.html``. It could look like this:

.. code-block:: django

    {% extends "admin/base.html" %}

    {% block extrahead %}
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.js" type="text/javascript"></script>
        {% include 'autocomplete_light/static.html' %}
    {% endblock %}

.. note::

    There is **nothing** magic in how the javascript loads. This means that you can
    use `django-compressor
    <https://github.com/jezdez/django_compressor>`_ or anything.

.. info::

    Also, why are we not using ``Widget.Media`` ? See  :doc:`FAQ</faq>`.
