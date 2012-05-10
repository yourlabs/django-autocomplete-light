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

Full documentation
------------------

.. toctree::
   :maxdepth: 3

   quick
   navigation
   forms

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
<https://github.com/yourlabs/django-autocomplete-light/issues>`_. Also, don't
hesitate to do pull requests !

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

