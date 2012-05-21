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

.. _remote-example:

Example
-------

In test_api_project, of course you should not hardcode urls like that in actual projects:

.. literalinclude:: ../../test_api_project/test_api_project/autocomplete_light_registry.py
   :language: python

Check out the documentation of :ref:`RemoteCountryChannel and
RemoteCityChannel<citieslight:remote-channel>` for more.

API
---

.. automodule:: autocomplete_light.channel.remote
   :members:

Javascript fun
--------------

Channels with `bootstrap='remote'` get a deck using `RemoteChannelDeck's
getValue()` rather than the default `getValue()` function.

.. literalinclude:: ../../autocomplete_light/static/autocomplete_light/remote.js
   :language: javascript
