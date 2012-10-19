Welcome to django-autocomplete-light's documentation!
=====================================================

Features
--------

This app fills all your ajax autocomplete needs:

- **global navigation** autocomplete :ref:`like on facebook
  <navigation>`
- **autocomplete widget** for :ref:`ModelChoiceField
  and ModelMultipleChoiceField<widget>`
- **GenericForeignKey** fully :ref:`supported<generic-fk>`
- **django-generic-m2m** support, yes that's a :ref:`generic M2M relation
  <generic-m2m>`!
- **CharField autocomplete** support, :ref:`comma separated values
  <charfield>`, useful for tags field,
- **APIs** powered autocomplete support, proposing :ref:`results that are not
  (yet) in the database<remote>`
- **0 hack** required for :ref:`admin integration<quick-admin>`, just use a
  form that uses the widget. It works exactly the same in the admin and in your
  pages.
- **no jQuery-ui** required, the autocomplete script is `as simple
  <_static/autocomplete.html>`_
  `as possible
  <_static/widget.html>`_,
- **optionnal** autocomplete :ref:`templating<template>`,
- **99%** of the python logic is encapsulated in "autocomplete" classes,
  :ref:`unlimited server side development possibilities
  <channel-view>`
- **99%** the javascript logic is encapsulated in an object, you can override any
  attribute or method, :ref:`unlimited client side development possibilities
  <javascript-fun>`
- **0 inline javascript** you can load the javascript just before </body> for
  best page loading performance, :ref:`wherever you want
  <javascript-setup>`
- **add another** :ref:`also available outside the admin<addanother>`,
- **simple** python, html and javascript, easy to hack, PEP8 compliant, tested

README
------

.. include:: ../../README.rst

Full documentation
------------------

.. toctree::
   :maxdepth: 1

   demo
   quick
   navigation
   forms
   template
   charfield
   addanother
   generic
   remote
   dependant
   django13

Javascript API
--------------

Work in progress:

- `autocomplete.js
  <_static/autocomplete.html>`_
- `widget.js
  <_static/widget.html>`_
- `addanother.js
  <_static/addanother.html>`_
- `remote.js
  <_static/remote.html>`_
- `text_widget.js
  <_static/text_widget.html>`_

.. _debugger:

When things go wrong
--------------------

There is a convenience view to visualize the registry, login as staff, and open
the autocomplete url, for example: /autocomplete_light/.

Ensure that:

- jquery is loaded,
- ``autocomplete_light/static.html`` is included once, it should load
  ``autocomplete.js``, ``widget.js`` and ``style.css``,
- your form uses autocomplete_light widgets,
- your channels are properly defined see ``/autocomplete/`` if you included
  ``autocomplete_light.urls`` with prefix ``/autocomplete/``.

If you don't know how to debug, you should learn to use:

Firebug javascript debugger
    Open the script tab, select a script, click on the left of the code to
    place a breakpoint

Ipdb python debugger
    Install ipdb with pip, and place in your python code: import ipdb; ipdb.set_trace()

If you are able to do that, then you are a professional, enjoy autocomplete_light !!!

If you need help, open an issue on the `github issues page
<https://github.com/yourlabs/django-autocomplete-light/issues>`_.

But make sure you've read `how to report bugs effectively
<http://www.chiark.greenend.org.uk/~sgtatham/bugs.html>`_
and `how to ask smart questions
<http://www.catb.org/~esr/faqs/smart-questions.html>`_.

Also, don't hesitate to do pull requests !

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

