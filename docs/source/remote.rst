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

RemoteChannel
-------------

.. automodule:: autocomplete_light.channel.remote
   :members:

Widget deck
-----------

Channels with `bootstrap='remote'` get a deck using `remoteGetValue()` rather
than the default `getValue()` function.

.. literalinclude:: ../../autocomplete_light/static/autocomplete_light/remote.js
   :language: javascript

Result template
---------------

As `RemoteChannelBase` extends `JSONChannelBase`, it uses
`autocomplete_light/result_with_json.html` by default:

.. literalinclude:: ../../autocomplete_light/templates/autocomplete_light/result_with_json.html
   :language: django
