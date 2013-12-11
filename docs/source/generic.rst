AutocompleteGeneric, for GenericForeignKey or GenericManyToMany
===============================================================

Generic relation support comes in two flavors:

- for django's generic foreign keys,
- and for django-generic-m2m's generic many to many in
  autocomplete_light.contrib.generic_m2m,

In v2, all you have to do is inherit from `autocomplete_light.ModelForm`.

If you don't want to use `autocomplete_light.ModelForm`
-------------------------------------------------------

TODO
