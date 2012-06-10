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
- ".deck" contains the list of selected item(s) as HTML,
- "input" should be the text input that has the Autocomplete,
- "select" a (optionnaly multiple) select
- ".remove" a (preferabely hidden) element that contains a value removal
 indicator, like an "X" sign or a trashcan icon, it is used to prefix every
 children of the deck
- ".item-template" a (preferabely hidden) element that contains the template
 for items which are added directly in the select, as they should be
 copied in the deck,

To avoid complexity, this script relies on extra HTML attributes, and
particularely one called 'data-value'. Learn more about data attributes:
http://dev.w3.org/html5/spec/global-attributes.html#embedding-custom-non-visible-data-with-the-data-attributes

When a suggestion is selected from the Autocomplete, its element is cloned
and appended to the deck - "deck" contains "items". It is important that the
suggestion elements of the autocomplete all contain a data-value attribute.
The value of data-value is used to fill the selected options in the hidden
select field.

If suggestions may not all have a data-value attribute, then you can
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
    this.itemTemplate = this.widget.find('.item-template li');

    // The number of items that the user may select with this widget. Set 0
    // for no limit. In the case of a foreign key you want to set it to 1.
    this.maxValues = 0;

    // When a suggestion is selected from the autocomplete of this widget,
    // getValue() is called to add and select the option in the select.
    this.getValue = function(suggestion) {
        return suggestion.data('value');
    };

    // The widget is in charge of managing its Autocomplete.
    this.initializeAutocomplete = function() {
        this.autocomplete = this.input.yourlabsAutocomplete(
            this.getAutocompleteOptions());
    };

    this.getAutocompleteOptions = function() {
        this.autocompleteOptions = {
            url: this.url,
            suggestionSelector: '.suggestion',
            minCharacters: this.minCharacters,
            placeholder: this.placeholder,
        }
    }

    // Bind Autocomplete.selectSuggestion signal to Widget.selectSuggestion()
    this.bindSelectSuggestion = function() {
        this.input.bind('selectSuggestion', function(e, suggestion) {
            if (!suggestion.length)
                return // placeholder: create suggestion here

            var widget = $(this).parents('.autocomplete-light-widget'
                ).yourlabsWidget();

            widget.selectSuggestion(suggestion);
        });
    };

    // Called when a suggestion is selected from the Autocomplete.
    this.selectSuggestion = function(suggestion) {
        // Get the value for this suggestion.
        var value = this.getValue(suggestion);

        if (!value) {
            if (window.console) console.log('yourlabs.Widget.getValue failed');
            return;
        }

        this.freeDeck();
        this.addToDeck(suggestion, value);
        this.addToSelect(suggestion, value);
        this.resetDisplay();

        this.input.val('');
    }

    // Unselect a value if the maximum number of selected values has been
    // reached.
    this.freeDeck = function() {
        var slots = this.maxValues - this.deck.children().length;

        if (this.maxValues && slots < 1) {
            // We'll remove the first item which is supposed to be the oldest
            var item = $(this.deck.children()[0]);

            // Unselect and remove the item's value from the select
            this.select.find(
                'option[data-value=' + item.attr('data-value') + ']'
            ).attr('selected', '').remove();

            // Actually remove the value from the deck
            item.remove();
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

    // Add a selected suggestion of a given value to the deck.
    this.addToDeck = function(suggestion, value) {
        var item = this.deck.find('[data-value='+value+']');

        // Avoid duplicating items in the deck.
        if (!item.length) {
            var item = suggestion.clone();

            // In case getValue() actually **created** the value, for example
            // with a post request.
            if (! item.attr('data-value')) {
                item.attr('data-value', value);
            }

            this.deck.append(item);

            // Append a clone of the .remove element.
            item.append(this.widget.find('.remove').clone());
        }
    }

    // Add a selected suggestion of a given value to the deck.
    this.addToSelect = function(suggestion, value) {
        var option = this.select.find('option[value='+value+']');

        if (! option.length) {
            this.select.append(
                '<option selected="selected" value="'+ value +'"></option>');
            option = this.select.find('option[value='+value+']');
        }

        option.attr('selected', 'selected');

        this.select.trigger('change');
    }

    // Called when the user clicks .remove in a deck item.
    this.deselectItem = function(item) {
        var value = this.getValue(item);

        this.select.find('option[value='+value+']').remove();
        this.select.trigger('change');

        item.remove();

        if (this.deck.children().length == 0) {
            this.deck.hide();
        }

        this.resetDisplay();
    };

    this.initialize = function() {
        var suggestions = this.deck.find('.suggestion');

        suggestions.append(this.widget.find('.remove:last').clone().show());
        if (this.payload.maxValues > 0 && suggestions.length == this.payload.maxValues) {
            this.input.hide();
        }

        this.initializeAutocomplete();
        this.bindSelectSuggestion();
    }
}

$.fn.yourlabsWidget = function(overrides) {
    var overrides = overrides ? overrides : {};
    var id = overrides.id || this.attr('id');

    if (id == undefined) {
        alert('Widget must have an id !');
        return;
    }

    if ($.fn.yourlabsWidget.registry == undefined) {
        $.fn.yourlabsWidget.registry = {};
    }

    if ($.fn.yourlabsWidget.registry[id] == undefined) {
        // Instanciate the widget
        $.fn.yourlabsWidget.registry[id] = new yourlabs.Widget(this);

        // Allow attribute overrides
        $.fn.yourlabsWidget.registry[id] = $.extend(
            $.fn.yourlabsWidget.registry[id], yourlabs.getDataOverrides());

        // Allow javascript object overrides
        $.fn.yourlabsWidget.registry[id] = $.extend(
            $.fn.yourlabsWidget.registry[id], overrides);

        // Setup for usage
        $.fn.yourlabsWidget.registry[id].initialize();

        // Set
        $.fn.yourlabsWidget.registry[id].widget.attr('data-widget-ready', 1);
        $.fn.yourlabsWidget.registry[id].widget.trigger('widget-ready');
    }

    return $.fn.yourlabsWidget.registry[id];
}

$(document).ready(function() {
    $('.autocomplete-light-widget[data-bootstrap=normal]').each(function() {
        /*
        Only setup widgets which have data-bootstrap=normal, if you want to
        initialize some Widgets with custom code, then set
        data-boostrap=yourbootstrap or something like that.
        */
        var deck = $(this).yourlabsWidget();
    });

    // Call Widget.deselectItem when .remove is clicked
    $('.autocomplete-light-widget .deck .remove').live('click', function() {
        var widget = $(this).parents('.autocomplete-light-widget');

        // I'd like to reproduce this and make sure it's necessary
        // if (!widget.length) return;

        var widget = $(this).parents('.autocomplete-light-widget'
            ).yourlabsWidget();

        var selector = widget.input.yourlabsAutocomplete().suggestionSelector;
        var suggestion = $(this).parents(selector);

        widget.deselectItem(suggestion);
    });

    /*
    Support values added directly in the select via js (ie. items created in
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

            function updateWidgetValue(value) {
                // is this necessary ?
                // if (!value) return;

                var item = widget.deck.find('[data-value='+value+']');

                if (!item.length) {
                    var item = widget.itemTemplate.clone();
                    var html = widget.select.find('option[value='+value+']').html();

                    suggestion.html(html);
                    suggestion.attr('data-value', value);

                    deck.selectSuggestion(suggestion);
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
});
