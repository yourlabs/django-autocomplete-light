Why not use Widget.Media ?
--------------------------

In the early versions (0.1) of django-autocomplete-light, we had widgets
defining the Media class like this:

.. code-block:: python

    class AutocompleteWidget(forms.SelectMultiple):
        class Media:
            js = ('autocomplete_light/autocomplete.js',)


This caused a problem if you want to load jquery and autocomplete.js globally
**anyway** and **anywhere** in the admin to have a global navigation
autocomplete: it would double load the scripts.

Also, this didn't work well with django-compressor and other cool ways of
deploying the JS.

So, in the next version, I added a dependency management system. Which sucked
and was removed right away to finally keep it simple and stupid as we have it
today.

How to ask for help ?
---------------------

The best way to ask for help is:

- fork the repo,
- add a simple way to reproduce your problem in a new app of test_project, try
  to keep it minimal,
- open an issue on github and mention your fork.

Really, it takes quite some time for me to clean pasted code and put up an
example app it would be really cool if you could help me with that !

If you don't want to do the fork and the reproduce case, then you should better
ask on StackOverflow and you might be lucky (just tag your question with
django-autocomplete-light to ensure that I find it).
