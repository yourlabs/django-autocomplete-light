Templating autocomplete_light
=============================

There are three templatetable pieces:

- the autocomplete box
- the widget which includes the deck
- results that are displayed in both the autocomplete box and the deck

The default template is autocomplete_light/autocomplete.html. That said, it
will try autocomplete_light/channelname/autocomplete.html

Basically, this means that if you copy autocomplete_light/autocomplete.html to
yourproject/templates/autocomplete_light/authorchannel/autocomplete.html, then
you should be able to customize the design of the Author autocomplete.

Note that this template calls channel.result_as_html to render a result. The
reason a result should be rendered individually by a channel is that it must be
rendered by both the autocomplete, but also the deck. The deck is the list of
selected options. You'll see it when the widget is rendered with initial values.

You can override autocomplete_light/result.html, but also
autocomplete_light/channelname/result.html. Same goes for widget.html.
