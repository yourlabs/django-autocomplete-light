Welcome to django-autocomplete-light's documentation!
=====================================================

Features
--------

This app fills all your ajax autocomplete needs:

- **global navigation** autocomplete like on http://betspire.com
- **autocomplete widget** for :ref:`ModelChoiceField
  and ModelMultipleChoiceField<widget>`
- **autocompletes that depend on each other**, :ref:`working
  example<citieslight:double-widget>` provided
- **GenericForeignKey** fully :ref:`supported<generic-fk>`
- **django-generic-m2m** support, yes that's a :ref:`generic M2M relation
  <generic-m2m>`!
- **APIs** powered autocomplete support, proposing :ref:`results that are not
  (yet) in the database<remote>`
- **very few code** was required to implement `this
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/autocomplete_light/channel/remote.py#L1>`_
  `kind
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/autocomplete_light/channel/generic.py#L1>`_
  `of
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/autocomplete_light/generic.py#L1>`__
  `features
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/autocomplete_light/contrib/generic_m2m.py#L1>`_
  , this app lets you satisfy the craziest autocomplete ideas your users
  might want, in a maintainable and sane way,
- **0 hack** required for :ref:`admin integration<quick-admin>`, just use a
  form that uses the widget. It works exactly the same in the admin and in your
  pages.
- **no jQuery-ui** required, the autocomplete script is `as simple
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/autocomplete_light/static/autocomplete_light/autocomplete.js>`_
  `as possible
  <https://github.com/yourlabs/django-autocomplete-light/blob/master/autocomplete_light/static/autocomplete_light/deck.js>`_,
- **all** the design of the autocompletes is encapsulated in template,
  :ref:`unlimited design possibilities<templates>`
- **99%** of the python logic is encapsulated in "channel" classes,
  :ref:`unlimited server side development possibilities
  <channel-view>`
- **99%** the javascript logic is encapsulated in an object, you can override any
  attribute or method, :ref:`unlimited client side development possibilities
  <javascript-fun>`
- **0 inline javascript** you can load the javascript just before </body> for
  best page loading performance, :ref:`wherever you want
  <javascript-setup>`
- **simple** python, html and javascript, easy to hack, PEP8 compliant
- **less sucking** code, no funny hacks, clean api, as few code as
  possible, that also means this is :ref:`not for pushovers<debugger>`

README
------

.. include:: ../../README.rst

Full documentation
------------------

.. toctree::
   :maxdepth: 3

   demo
   quick
   navigation
   forms
   generic
   remote
   django13

Javascript API
--------------

Work in progress:

- `autocomplete.js
  <_static/autocomplete.html>`_
- `deck.js
  <_static/deck.html>`_

.. _debugger:

When things go wrong
--------------------

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

