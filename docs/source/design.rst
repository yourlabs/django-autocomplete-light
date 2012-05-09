Global design
=============

Every piece of the app is described here along with the number of Single
Line Of Code (SLOC) as this is the kind of things that weights when I
decide which app I want to use.

Don't worry if you don't get it all at once, this is merely an
inventory of what's there and why. Refer to other pages of the
documentations for gory details. 

Two javascript files, two jQuery extensions
-------------------------------------------

static/autocomplete_light/autocomplete.js
    The yourlabs_autocomplete jQuery extension, it's required for any
    kind of autocomplete, navigation or form fields. ~200 SLOC.

static/autocomplete_light/deck.js
    The yourlabs_deck jQuery extension, it's required for the
    AutocompleteWidget, for forms. It is not required if you just want a
    global navigation autocomplete.  ~150 SLOC.

One view, one url
-----------------

.. autoclass:: autocomplete_light.views.ChannelView
   :members: get

autocomplete_light_channel
    This url takes a keyword argument, *channel*, which is the name of
    the channel to use.

One widget
----------

.. autoclass:: autocomplete_light.widgets.AutocompleteWidget
   :members:

Channels
--------

Channel classes encapsulate the python logic required for the python
AutocompleteWidget. It is not required if you just want a global
navigation autocomplete.

For example, if you want autocomplete for models Author and Book, then
you'll want to register at least two channels: AuthorChannel and
BookChannel.

We provide two base channels:

.. autoclass:: autocomplete_light.channel.base.ChannelBase
   :members:

.. autoclass:: autocomplete_light.channel.json.JSONChannelBase
   :members:

Registry
--------

The registry is in charge of autodiscovering and carrying the list of
declared channels, like `django.contrib.admin`.

Like django admin, you can just register a model, and the channel will
be generated for you.

.. automodule:: autocomplete_light.registry
   :members:

Forms
-----

For convenience, a couple of helpers to enable autocomplete widgets eeasily in forms:

.. automodule:: autocomplete_light.forms
   :members:

32 SLOC

Clean API
---------

Just import autocomplete_light, you can access any element from there.
For example::

    import autocomplete_light

    autocomplete_light.ChannelBase
    autocomplete_light.JSONChannelBase
    autocomplete_light.modelform_factory
    autocomplete_light.register
    autocomplete_light.AutocompleteWidget
    # etc, etc ...
