Doing funny things
==================

My client wanted me to do funny things, so that's the reason I needed an
autocomplete app that's simple enought to stay out of my way. You could replace
the term 'funny' by 'painful'.

Let's review some of the funny things you could do.

Overriding autocomplete or deck options
---------------------------------------

Behind the scenes, deck.js initializes a deck for each autocomplete widget, and
the autocomplete for the text input in that widget. Default options are passed.

In the default result template, autocomplete_light/result.html, you can see
that the result tag has a special attribute, *data-value*::

    <li class="result" data-value="{{ result.pk }}">

Which works well because the default getValue callback for the deck is::

    'getValue': function(deck, result) {
        return result.data('value');
    },

Let's say that it gets in your way, that it's not what you want. That you want
to implement your own getValue callback because you want to satisfy your funny
client.

Remember when you've read that that deck.js initializes a deck for all autocomplete widgets ? Well that's not completely true.

In deck.js, you can see how it's bootstrapped with no custom options::

    $('.autocomplete_light_widget[data-bootstrap=normal]').each(function() {
        $(this).yourlabs_deck();
    });

Note that it only bootstraps widgets with data-bootstrap=normal. So, suppose
that your channel class has a bootstrap attribute as such::

    class FunnyChannel(ChannelBase):
        bootstrap = 'funny'

Then, deck.js will not initialize the deck and autocomplete for widgets using
this channel. Which means that you could safely initialize the deck with the
overrides you want::

    $(document).ready(function() {
        $('.autocomplete_light_widget[data-bootstrap=funny]').each(function() {
            $(this).yourlabs_deck({
                getValue: function(deck, result) {
                    // find funny ways to return the value (object pk in most cases)
                    return ...;
                },
                autocompleteOptions: {
                    defaultValue: 'Welcome to the funny autocomplete',
                },
            });
        });
    });

What happens in yourlabs_deck or yourlabs_autocomplete extensions, is that:

- it will return the existing deck or autocomplete for the element if it already exists
- otherwise, it will instanciate one, merge the array that was passed as
  argument if any, and then call the initialize() method, which means that you
  can override any attribute or method

Funny example: autocompletes that depend on each others
-------------------------------------------------------

Consider `django-cities-light models
<https://github.com/yourlabs/django-cities-light/blob/master/cities_light/models.py>`_.
There is a Country and a City model.

If you have an Address model with an FK to City, then there is no need for
Address to have an FK to Country. Because you could get the country of an
address with address.city.country.

However, there are many cities called "Paris". So you could either make your
city results display as 'Paris (France)', either have a multiwidget with two
autocompletes:

- one to select the country
- one to select the city, that proposes cities filtered by the selected country

That's exactly what `CityAutocompleteWidget
<https://github.com/yourlabs/django-cities-light/blob/master/cities_light/widgets.py>`_
does.

Check out the pieces used to achieve such a result:

- `CityAutocompleteWidget multi widget, includes two AutocompleteWidget
  <https://github.com/yourlabs/django-cities-light/blob/master/cities_light/widgets.py>`_,
- `Custom bootstrap for that widget (countrycity)
  <https://github.com/yourlabs/django-cities-light/blob/master/cities_light/static/cities_light/autocomplete_light.js>`_,
- `Custom query_filter for CityChannel
  <https://github.com/yourlabs/django-cities-light/blob/master/cities_light/autocomplete_light_registry.py>`_,

When things go wrong
--------------------

If you don't know how to debug, you should learn to use:

Firebug javascript debugger
    Open the script tab, select a script, click on the left of the code to
    place a breakpoint

Ipdb python debugger
    Install ipdb with pip, and place in your python code: import ipdb; ipdb.set_trace()

If you are able to do that, then you are a professional, enjoy autocomplete_light !!!
