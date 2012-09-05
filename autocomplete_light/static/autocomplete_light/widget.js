/*
Widget complements Autocomplete by enabling autocompletes to be used as
value holders. It looks very much like Autocomplete in its design. Thus, it
is recommended to read the source of Autocomplete first.

Widget behaves like the autocomplete in facebook profile page, which all
users should be able to use.

Behind the scenes, Widget maintains a normal hidden select which makes it
simple to play with on the server side like on the client side. If a value
is added and selected in the select element, then it is added to the deck,
and vice-versa.

It needs some elements, and established vocabulary:

- ".autocomplete-light-widget" element wraps all the HTML necessary for the
 widget,
- ".deck" contains the list of selected choice(s) as HTML,
- "input" should be the text input that has the Autocomplete,
- "select" a (optionnaly multiple) select
- ".remove" a (preferabely hidden) element that contains a value removal
 indicator, like an "X" sign or a trashcan icon, it is used to prefix every
 children of the deck
- ".choice-template" a (preferabely hidden) element that contains the template
 for choices which are added directly in the select, as they should be
 copied in the deck,

To avoid complexity, this script relies on extra HTML attributes, and
particularely one called 'data-value'. Learn more about data attributes:
http://dev.w3.org/html5/spec/global-attributes.html#embedding-custom-non-visible-data-with-the-data-attributes

When a choice is selected from the Autocomplete, its element is cloned
and appended to the deck - "deck" contains "choices". It is important that the
choice elements of the autocomplete all contain a data-value attribute.
The value of data-value is used to fill the selected options in the hidden
select field.

If choices may not all have a data-value attribute, then you can
override Widget.getValue() to implement your own logic.
*/

// Our class will live in the yourlabs global namespace.
if (window.yourlabs == undefined) window.yourlabs = {};

/*
Instanciate a Widget.
*/
yourlabs.Widget = function(widget) {
    // These attributes where described above.
    this.widget = widget;
    this.input = this.widget.find('input');
    this.select = this.widget.find('select');
    this.deck = this.widget.find('.deck');
    this.choiceTemplate = this.widget.find('.choice-template .choice');

    // The number of choices that the user may select with this widget. Set 0
    // for no limit. In the case of a foreign key you want to set it to 1.
    this.maxValues = 0;

    // When a choice is selected from the autocomplete of this widget,
    // getValue() is called to add and select the option in the select.
    this.getValue = function(choice) {
        return choice.attr('data-value');
    };

    // The widget is in charge of managing its Autocomplete.
    this.initializeAutocomplete = function() {
        this.autocomplete = this.input.yourlabsAutocomplete(
            this.autocompleteOptions);

        // Add a class to ease css selection of autocompletes for widgets
        this.autocomplete.outerContainer.addClass(
            'autocomplete-light-widget');
    };

    // Bind Autocomplete.selectChoice signal to Widget.selectChoice()
    this.bindSelectChoice = function() {
        this.input.bind('selectChoice', function(e, choice) {
            if (!choice.length)
                return // placeholder: create choice here

            var widget = $(this).parents('.autocomplete-light-widget'
                ).yourlabsWidget();

            widget.selectChoice(choice);
        });
    };

    // Called when a choice is selected from the Autocomplete.
    this.selectChoice = function(choice) {
        // Get the value for this choice.
        var value = this.getValue(choice);

        if (!value) {
            if (window.console) console.log('yourlabs.Widget.getValue failed');
            return;
        }

        this.freeDeck();
        this.addToDeck(choice, value);
        this.addToSelect(choice, value);
        this.resetDisplay();

        this.input.val('');
    }

    // Unselect a value if the maximum number of selected values has been
    // reached.
    this.freeDeck = function() {
        var slots = this.maxValues - this.deck.children().length;

        if (this.maxValues && slots < 1) {
            // We'll remove the first choice which is supposed to be the oldest
            var choice = $(this.deck.children()[0]);

            this.deselectChoice(choice);
        }
    }

    // Empty the search input and hide it if maxValues has been reached.
    this.resetDisplay = function() {
        var selected = this.select.find('option:selected').length;

        if (this.maxValues && selected == this.maxValues) {
            this.input.hide();
        } else {
            this.input.show();
        }

        this.deck.show();
    }

    // Add a selected choice of a given value to the deck.
    this.addToDeck = function(choice, value) {
        var existing_choice = this.deck.find('[data-value="'+value+'"]');

        // Avoid duplicating choices in the deck.
        if (!existing_choice.length) {
            var choice = choice.clone();

            // In case getValue() actually **created** the value, for example
            // with a post request.
            choice.attr('data-value', value);

            this.deck.append(choice);

            // Append a clone of the .remove element.
            choice.prepend(this.widget.find('.remove:not(:visible)').clone().show());
        }
    }

    // Add a selected choice of a given value to the deck.
    this.addToSelect = function(choice, value) {
        var option = this.select.find('option[value="'+value+'"]');

        if (! option.length) {
            this.select.append(
                '<option selected="selected" value="'+ value +'"></option>');
            option = this.select.find('option[value="'+value+'"]');
        }

        option.attr('selected', 'selected');

        this.select.trigger('change');
    }

    // Called when the user clicks .remove in a deck choice.
    this.deselectChoice = function(choice) {
        var value = this.getValue(choice);

        this.select.find('option[value="'+value+'"]').remove();
        this.select.trigger('change');

        choice.remove();

        if (this.deck.children().length == 0) {
            this.deck.hide();
        }

        this.resetDisplay();
    };

    this.initialize = function() {
        this.initializeAutocomplete();

        // Working around firefox tempering form values after reload
        var widget = this;
        this.deck.find(this.autocomplete.choiceSelector).each(function() {
            var value = widget.getValue($(this));
            var option = widget.select.find('option[value="'+value+'"]');
            if (!option.attr('selected')) option.attr('selected', true);
        });

        var choices = this.deck.find(
            this.input.yourlabsAutocomplete().choiceSelector);

        // Add the remove icon to each choice
        choices.prepend(this.widget.find('.remove:last').clone().show());
        this.resetDisplay();

        this.bindSelectChoice();
    }
}

$.fn.yourlabsWidget = function(overrides) {
    var overrides = overrides ? overrides : {};

    if (this.data('widget') == undefined) {
        // Instanciate the widget
        var widget = new yourlabs.Widget(this);

        // Pares data-*
        var data = this.data();
        var dataOverrides = {autocompleteOptions: {}};
        for (var key in data) {
            if (!key) continue;

            if (key.substr(0, 12) == 'autocomplete') {
                var newKey = key.replace('autocomplete', '');
                newKey = newKey.replace(newKey[0], newKey[0].toLowerCase())
                dataOverrides['autocompleteOptions'][newKey] = data[key];
            } else {
                dataOverrides[key] = data[key];
            }
        }

        // Allow attribute overrides
        widget = $.extend(widget, dataOverrides);

        // Allow javascript object overrides
        widget = $.extend(widget, overrides);

        this.data('widget', widget);

        // Setup for usage
        widget.initialize();

        // Widget is ready
        widget.widget.attr('data-widget-ready', 1);
        widget.widget.trigger('widget-ready');
    }

    return this.data('widget');
}

$(document).ready(function() {
    $('.autocomplete-light-widget[data-bootstrap=normal]').live('initialize', function() {
        /*
        Only setup widgets which have data-bootstrap=normal, if you want to
        initialize some Widgets with custom code, then set
        data-boostrap=yourbootstrap or something like that.
        */
        $(this).yourlabsWidget();
    });

    // Call Widget.deselectChoice when .remove is clicked
    $('.autocomplete-light-widget .deck .remove').live('click', function() {
        var widget = $(this).parents('.autocomplete-light-widget'
            ).yourlabsWidget();

        var selector = widget.input.yourlabsAutocomplete().choiceSelector;
        var choice = $(this).parents(selector);

        widget.deselectChoice(choice);
    });

    /*
    Support values added directly in the select via js (ie. choices created in
    modal or popup).

    For this, we make one timer that regularely checks for values in the select
    that are not in the deck. The reason for that is that change is not triggered
    when options are added like this:

        $('select#id-dependencies').append(
            '<option value="9999" selected="selected">blabla</option>')

    Sorry for the hack but I see no other way, this is HTML's fault.
    */
    function updateWidgets() {
        $('.autocomplete-light-widget[data-widget-ready=1]').each(function() {
            var widget = $(this).yourlabsWidget();
            var value = widget.select.val();

            if (!value) return;

            function updateWidgetValue(value) {
                // is this necessary ?
                // if (!value) return;

                var choice = widget.deck.find('[data-value="'+value+'"]');

                if (!choice.length) {
                    var choice = widget.choiceTemplate.clone();
                    var html = widget.select.find('option[value="'+value+'"]').html();

                    choice.html(html);
                    choice.attr('data-value', value);

                    widget.selectChoice(choice);
                }
            }

            if (value instanceof Array) {
                for(var i=0; i<value.length; i++) {
                    updateWidgetValue(value[i]);
                }
            } else {
                updateWidgetValue(value);
            }
        });
        setTimeout(updateWidgets, 2000);
    }
    setTimeout(updateWidgets, 1000);

    // Solid initialization, usage:
    //
    //      $(document).bind('yourlabsWidgetReady', function() {
    //          $('.your.autocomplete-light-widget').live('initialize', function() {
    //              $(this).yourlabsWidget({
    //                  yourCustomArgs: // ...
    //              })
    //          });
    //      });
    $(document).trigger('yourlabsWidgetReady');

    $('.autocomplete-light-widget:not([id*="__prefix__"])').each(function() {
        $(this).trigger('initialize');
    });

    $(document).bind('DOMNodeInserted', function(e) {
        var widget = $(e.target).find('.autocomplete-light-widget');

        if (!widget.length) {
            widget = $(e.target).is('.autocomplete-light-widget') ? $(e.target) : false;

            if (!widget) {
                return;
            }
        }

        widget.trigger('initialize');
    });
});
