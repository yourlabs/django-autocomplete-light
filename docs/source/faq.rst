Why not use Widget.Media ?
--------------------------

In the early versions (0.x) of django-autocomplete-light, we had widgets
defining the Media class like this:



This caused a problem if you want to load jquery and autocomplete.js globally
**anyway** and **anywhere** in the admin to have a global navigation
autocomplete: it would double load the scripts.

So, in the next version, I added a dependency management system. Which sucked
and was removed right away to finally keep it simple and stupid as we have it
today.

Also, this doesn't work well with django-compressor and other cool ways of
deploying the JS.
