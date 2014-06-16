.. _charfield:

CharField autocompletes
=======================

`django-tagging
<http://code.google.com/p/django-tagging/>`_ and derivates like `django-tagging-ng
<https://github.com/svetlyak40wt/django-tagging-ng>`_ provide a ``TagField``,
which is a ``CharField`` expecting comma separated tags. Behind the scenes,
this field is parsed and ``Tag`` model instances are created and/or linked.

A stripped variant of ``widget.js``, ``text_widget.js``, enables autocompletion
for such a field. To make it even easier, a stripped variant of ``Widget``,
``TextWidget``, automates configuration of ``text_widget.js``.

Needless to say, ``TextWidget`` and  ``text_widget.js`` have a structure that
is consistent with ``Widget`` and ``widget.js``.

It doesn't have many features for now, but feel free to participate to the
`project on GitHub
<https://github.com/yourlabs/django-autocomplete-light>`_.

As usual, a working example lives in test_project. in app
``charfield_autocomplete``.

.. Warning::
    Note that this feature was added in version 1.0.16, if you have overloaded
    ``autocomplete_light/static.html`` from a previous version then you should
    make it load ``autocomplete_light/text_widget.js`` to get this new feature.

Example
-------

This demonstrates a working usage of TextWidget:

.. literalinclude:: ../../autocomplete_light/example_apps/charfield_autocomplete/forms.py
   :language: python

FTR, using the form in the admin is still as easy:

.. literalinclude:: ../../autocomplete_light/example_apps/charfield_autocomplete/admin.py
   :language: python

So is registering an Autocomplete for Tag:

.. literalinclude:: ../../autocomplete_light/example_apps/charfield_autocomplete/autocomplete_light_registry.py
   :language: python

Django-tagging
--------------

This demonstrates the models setup used for the above example, using
django-taggit, which provides a normal CharField behaviour:

.. literalinclude:: ../../autocomplete_light/example_apps/charfield_autocomplete/models.py
   :language: python

Django-taggit
-------------

For `django-taggit
<http://pypi.python.org/pypi/django-taggit>`_,
you need
:doc:`autocomplete_light.contrib.taggit_tagfield
<contrib>`.
