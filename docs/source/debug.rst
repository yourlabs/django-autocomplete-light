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


