This is a simple alternative to django-ajax-selects.

What's the difference ?
-----------------------

- it relies on a 207 SLOC script for autocompletion, rather than jQuery-ui
  bloatware
- 83 SLOC to manage the result deck, very customizable: almost all the logic is
  in options
- the autocompletion script is also very good to create a global navigation
  autocomplete (actually it comes from betspire.com)
- use a template to render the autocomplete, simple and pretty
- very few logic in the app, all the logic is delegated to the channel class
  which you can implement as you wish
- (simple) admin-like registration
- does not force to load jquery and dependencies at the top of the page, you
  can leave the javascript just before </body> and get better page load
- use django's ModelChoiceField and AutocompleteWidget
- straight to the point, for hardcore webdevs with imagination

Status
------

The API is subject to many changes until the release. Probably half of the
features we need are missing.
