Welcome to django-autocomplete-light's documentation!
=====================================================

Features
--------

This app fills all your ajax autocomplete needs:

- global navigation autocomplete like on http://betspire.com
- autocomplete widget for ModelChoiceField and ModelMultipleChoiceField
- **0 hack** required for admin integration, just use a form that uses the
  widget
- **no jQuery-ui** required, the autocomplete script is as simple as possible
- **all** the design of the autocompletes is encapsulated in template,
  unlimited design possibilities
- **99%** of the python logic is encapsulated in "channel" classes, unlimited
  development possibilities
- **99%** the javascript logic is encapsulated in an "options" array, 
  unlimited development possibilities
- **no** inline javascript, you can load the javascript just before </body> for
  best page loading performance
- **simple** python, html and javascript, easy to hack
- **less sucking** code, no funny hacks, clean api, as few code as
  possible, that also means this is not for pushovers

So, if you know django-ajax-selects, it does the same thing, and much
more, with half the code of django-ajax-selects.

Contents
--------

.. toctree::
   :maxdepth: 2

   design
   install
   navigation
   forms
   admin
   funny

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

