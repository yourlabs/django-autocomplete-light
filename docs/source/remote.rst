Proposing results from a remote API
===================================

This documentation is optionnal, but it is complementary with all other
documentation. It aims advanced users.

Consider a social network about music. In order to propose all songs in the
world in its autocomplete, it should either:

- have a database with all songs of the world,
- use a simple REST API to query a database with all songs world

The purpose of this documentation is to describe every elements involved. Note
that a living demonstration is available in `test_api_project`, where one
project serves a full database of cities via an API to another.


Example
-------

In test_api_project, of course you should not hardcode urls like that in actual projects:

.. literalinclude:: ../../test_api_project/test_api_project/autocomplete_light_registry.py
   :language: python

For details on how these channels are created, have a look at
`autocomplete stuff in django-cities-light contrib folder
<https://github.com/yourlabs/django-cities-light/tree/master/cities_light/contrib>`_.

API
---

.. automodule:: autocomplete_light.channel.remote
   :members:

Gory details
------------

Channels with `bootstrap='remote'` get a deck using `remoteGetValue()` rather
than the default `getValue()` function.

.. literalinclude:: ../../autocomplete_light/static/autocomplete_light/remote.js
   :language: javascript
