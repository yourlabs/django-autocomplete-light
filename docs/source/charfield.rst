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

Example
-------

This demonstrates a working usage of TextWidget:

.. literalinclude:: ../../test_project/charfield_autocomplete/forms.py
   :language: python

FTR, using the form in the admin is still as easy:

.. literalinclude:: ../../test_project/charfield_autocomplete/admin.py
   :language: python

So is registering an Autocomplete for Tag:

.. literalinclude:: ../../test_project/charfield_autocomplete/autocomplete_light_registry.py
   :language: python

Upgrading from previous versions
--------------------------------

This feature is available since version 1.0.16.

Note that if you have customized ``autocomplete_light/static.html``, you have
to update it to include ``text_widget.js``. FTR, this is what it looks like:

.. literalinclude:: ../../autocomplete_light/templates/autocomplete_light/static.html
   :language: django
