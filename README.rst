This is a simple alternative to django-ajax-selects.

Read the documentation on http://readthedocs.org/docs/django-autocomplete-light/en/latest/

What's the difference ?
-----------------------

- it relies on a small, simple, easy to read script that allows you to override
  any attribute for autocompletion, rather than jQueryUi bloatware (203 SLOC)
- the autocompletion script is also very good to create a global navigation
  autocomplete (actually it comes from betspire.com)
- another script is in charge of the result deck, it follows the same flexible
  pattern than the autocomplete script (130 SLOC)
- use a template to render the autocomplete, simple and pretty
- very few logic in the app, all the logic is delegated to the channel class
  which you can implement as you wish
- (simple) admin-like registration
- does not force to load jquery and dependencies at the top of the page, you
  can leave the javascript just before </body> and get better page load
- support django's ModelChoiceField and AutocompleteWidget
- support autocompletes that depend on each other (see documentation on doing
  'funny' things)
- straight to the point, for hardcore webdevs with imagination

Status
------

The API is not subject to many changes until the release. We've got pretty much
everything we want except the design which is being worked on at the time of
writing.
