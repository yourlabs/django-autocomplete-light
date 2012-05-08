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
    kind of autocomplete, navigation or form fields. 211 SLOC.

static/autocomplete_light/deck.js
    The yourlabs_deck jQuery extension, it's required for the
    AutocompleteWidget, for forms. It is not required if you just want a
    global navigation autocomplete. 127 SLOC.

One view, one url
-----------------

views.ChannelView
    The ChannelView routes the request to the proper channel, and
    returns the result from channel.render_autocomplete(). As mentionned
    in the feature list, all the logic is delegated to the channel so
    that it doesn't get in your way. 6 SLOC.

autocomplete_light_channel
    This url takes a keyword argument, *channel*, which is the name of
    the channel to use. 3 SLOC.

One widget
----------

widgets.AutocompleteWidget
    This widget works for both ModelChoiceField and ModelMultipleChoice
    field. This widget has one required option: 'channel_name'. Another
    important option is 'max_items' which should be set to 1 for a
    ModelChoiceField. It is unlikely that you need to extend it, as it
    barely serves as connector between the form field and the channel,
    and relies on templates for rendering. 50 SLOC

Channels
--------

Channel classes encapsulate the python logic required for the python
AutocompleteWidget. It is not required if you just want a global
navigation autocomplete.

For example, if you want autocomplete for models Author and Book, then
you'll want to register at least two channels: AuthorChannel and
BookChannel.

We provide two base channels:

channel.base.ChannelBase
    This is the base channel class. It is in charge of:
    - fetching the results for a query
    - rendering the autocomplete with a template
    - rendering results in the autocomplete with a template
    - validating input
    Only 62 SLOC.

channel.json.JSONChannelBase
    This channel adds a couple of features:
    - making a dict from a result, the dict can contain any data you
    want, you'll be able to use it in your javascript
    - returning the json from a result dict
    17 SLOC.

Registry
--------

The registry is in charge of autodiscovering and carrying the list of
declared channels, like `django.contrib.admin`.

Like django admin, you can just register a model, and the channel will
be generated for you.

registry.ChannelRegistry
    This class extends python's dict type, it provides two simple
    methods: `register(model, channel=None)`, and
    `channel_for_model(model)`. You probably won't need to use it at
    all.

registry.registry
    Is a global instance of ChannelRegistry.

registry.register(model, channel=None)
    Is a shortcut to register a channel.

registry.autodiscover()
    Attempts to import `autocomplete_light_registry` from all installed
    apps. You'll want to call it from your urls module **before** you
    run `django.contrib.admin.autodiscover()` because your modeladmins
    might use forms that use autocompletes.

34 SLOC.

Forms
-----

For convenience, a couple of helpers to enable autocomplete widgets eeasily in forms:

forms.get_widgets_dict(model, autocomplete_exclude=None)
    This method will return a dict of widget `usable by
    Django<https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-field-types-or-widgets>_`
    for a given model class. Basically, it inspects the model class for
    foreign keys and many to many relations, and relies on the
    ChannelRegistry.channel_for_model() to instanciate an
    AutocompleteWidget with the appropriate channel.

forms.modelform_factory(model, autocomplete_exclude=None, kwargs)
    This function decorates Django's modelform_factory, but also uses
    forms.get_widgets_dict(). This means that if you use
    forms.modelform_factory rather than Django's modelform_factory,
    you'll get the same result except that the form will use as much
    autocompletes as possible.

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
