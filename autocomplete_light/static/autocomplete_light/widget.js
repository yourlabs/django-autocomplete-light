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

$.ajaxSettings.traditional = true

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
    this.maximumValues = 0;
    
    // Clear input when choice made? 1 for yes, 0 for no
    this.clearInputOnSelectChoice = "1";
}

// When a choice is selected from the autocomplete of this widget,
// getValue() is called to add and select the option in the select.
yourlabs.Widget.prototype.getValue = function(choice) {
    return choice.attr('data-value');
};

// The widget is in charge of managing its Autocomplete.
yourlabs.Widget.prototype.initializeAutocomplete = function() {
    this.autocomplete = this.input.yourlabsAutocomplete()

    // Add a class to ease css selection of autocompletes for widgets
    this.autocomplete.box.addClass('autocomplete-light-widget');
};

// Bind Autocomplete.selectChoice signal to Widget.selectChoice()
yourlabs.Widget.prototype.bindSelectChoice = function() {
    this.input.bind('selectChoice', function(e, choice) {
        if (!choice.length)
            return // placeholder: create choice here

        var widget = $(this).parents('.autocomplete-light-widget'
            ).yourlabsWidget();

        widget.selectChoice(choice);
    });
};

// Called when a choice is selected from the Autocomplete.
yourlabs.Widget.prototype.selectChoice = function(choice) {
    // Get the value for this choice.
    var value = this.getValue(choice);

    if (!value) {
        if (window.console) console.log('yourlabs.Widget.getValue failed');
        return;
    }

    this.freeDeck();
    this.addToDeck(choice, value);
    this.addToSelect(choice, value);
    
    var index = $(':input:visible').index(this.input);
    this.resetDisplay();

    if (this.input.is(':visible')) {
        this.input.focus();
    } else {
        var next = $(':input:visible:eq('+ index +')');
        next.focus();
    }

    if (this.clearInputOnSelectChoice === "1")
        this.input.val('');
}

// Unselect a value if the maximum number of selected values has been
// reached.
yourlabs.Widget.prototype.freeDeck = function() {
    var slots = this.maximumValues - this.deck.children().length;

    if (this.maximumValues && slots < 1) {
        // We'll remove the first choice which is supposed to be the oldest
        var choice = $(this.deck.children()[0]);

        this.deselectChoice(choice);
    }
}

// Empty the search input and hide it if maximumValues has been reached.
yourlabs.Widget.prototype.resetDisplay = function() {
    var selected = this.select.find('option:selected').length;

    if (this.maximumValues && selected == this.maximumValues) {
        this.input.hide();
    } else {
        this.input.show();
    }

    this.deck.show();

    // Also fix the position if the autocomplete is shown.
    if (this.autocomplete.box.is(':visible')) this.autocomplete.fixPosition();
}

yourlabs.Widget.prototype.deckChoiceHtml = function(choice, value) {
    var deckChoice = choice.clone();

    this.addRemove(deckChoice);

    return deckChoice;
}

yourlabs.Widget.prototype.optionChoice = function(option) {
    var optionChoice = this.choiceTemplate.clone();
    
    var target = optionChoice.find('.append-option-html');

    if (target.length) {
        target.append(option.html());
    } else {
        optionChoice.html(option.html());
    }

    return optionChoice;
}

yourlabs.Widget.prototype.addRemove = function(choices) {
    var removeTemplate = this.widget.find('.remove:last')
        .clone().css('display', 'inline-block');

    var target = choices.find('.prepend-remove');

    if (target.length) {
        target.prepend(removeTemplate);
    } else {
        // Add the remove icon to each choice
        choices.prepend(removeTemplate);
    } 
}

// Add a selected choice of a given value to the deck.
yourlabs.Widget.prototype.addToDeck = function(choice, value) {
    var existing_choice = this.deck.find('[data-value="'+value+'"]');

    // Avoid duplicating choices in the deck.
    if (!existing_choice.length) {
        var deckChoice = this.deckChoiceHtml(choice);

        // In case getValue() actually **created** the value, for example
        // with a post request.
        deckChoice.attr('data-value', value);

        this.deck.append(deckChoice);
    }
}

// Add a selected choice of a given value to the deck.
yourlabs.Widget.prototype.addToSelect = function(choice, value) {
    var option = this.select.find('option[value="'+value+'"]');

    if (! option.length) {
        this.select.append(
            '<option selected="selected" value="'+ value +'"></option>');
        option = this.select.find('option[value="'+value+'"]');
    }

    option.attr('selected', 'selected');

    this.select.trigger('change');
    this.updateAutocompleteExclude();
}

// Called when the user clicks .remove in a deck choice.
yourlabs.Widget.prototype.deselectChoice = function(choice) {
    var value = this.getValue(choice);

    this.select.find('option[value="'+value+'"]').remove();
    this.select.trigger('change');

    choice.remove();

    if (this.deck.children().length == 0) {
        this.deck.hide();
    }

    this.updateAutocompleteExclude();
    this.resetDisplay();
};

yourlabs.Widget.prototype.updateAutocompleteExclude = function() {
    var widget = this;
    var choices = this.deck.find(this.autocomplete.choiceSelector);

    this.autocomplete.data['exclude'] = $.map(choices, function(choice) { 
        return widget.getValue($(choice)); 
    });
}

yourlabs.Widget.prototype.initialize = function() {
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

    this.addRemove(choices);
    this.resetDisplay();

    this.bindSelectChoice();
    this.clearBoth()
}

// Add an empty div with clear:both after the widget's container.
// This is meant to support django-responsive-admin templates.
yourlabs.Widget.prototype.clearBoth = function() {
    this.widget.parent().append('<div style="clear: both"></div>');
}

// Destroy the widget. Takes a widget element because a cloned widget element
// will be dirty, ie. have wrong .input and .widget properties.
yourlabs.Widget.prototype.destroy = function(widget) {
    widget.find('input')
        .unbind('selectChoice')
        .yourlabsAutocomplete('destroy');
}

// Get or create or destroy a widget instance.
//
// On first call, yourlabsWidget() will instanciate a widget applying all
// passed overrides.
// 
// On later calls, yourlabsWidget() will return the previously created widget
// instance, which is stored in widget.data('widget').
//
// Calling yourlabsWidget('destroy') will destroy the widget. Useful if the
// element was blindly cloned with .clone(true) for example.
$.fn.yourlabsWidget = function(overrides) {
    var overrides = overrides ? overrides : {};

    var widget = this.yourlabsRegistry('widget');

    if (overrides == 'destroy') {
        if (widget) {
            widget.destroy(this);
            this.removeData('widget');
        }
        return
    }

    if (widget == undefined) {
        // Instanciate the widget
        var widget = new yourlabs.Widget(this);

        // Extend the instance with data-widget-* overrides
        for (var key in this.data()) {
            if (!key) continue;
            if (key.substr(0, 6) != 'widget' || key == 'widget') continue;
            var newKey = key.replace('widget', '');
            var newKey = newKey.charAt(0).toLowerCase() + newKey.slice(1);
            widget[newKey] = this.data(key);
        }

        // Allow javascript object overrides
        widget = $.extend(widget, overrides);

        $(this).yourlabsRegistry('widget', widget);

        // Setup for usage
        widget.initialize();

        // Widget is ready
        widget.widget.attr('data-widget-ready', 1);
        widget.widget.trigger('widget-ready');
    }

    return widget;
}

$(document).ready(function() {
    $('body').on('initialize', '.autocomplete-light-widget[data-widget-bootstrap=normal]', function() {
        /*
        Only setup widgets which have data-widget-bootstrap=normal, if you want to
        initialize some Widgets with custom code, then set
        data-widget-boostrap=yourbootstrap or something like that.
        */
        $(this).yourlabsWidget();
    });

    // Call Widget.deselectChoice when .remove is clicked
    $('body').on('click', '.autocomplete-light-widget .deck .remove', function() {
        var widget = $(this).parents('.autocomplete-light-widget'
            ).yourlabsWidget();

        var selector = widget.input.yourlabsAutocomplete().choiceSelector;
        var choice = $(this).parents(selector);

        widget.deselectChoice(choice);
    });

    // Solid initialization, usage:
    //
    //
    //      $(document).bind('yourlabsWidgetReady', function() {
    //          $('.your.autocomplete-light-widget').on('initialize', function() {
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
        /*
        Support values added directly in the select via js (ie. choices created in
        modal or popup).

        For this, we listen to DOMNodeInserted and intercept insert of <option> nodes.
        
        The reason for that is that change is not triggered when options are
        added like this:

            $('select#id-dependencies').append(
                '<option value="9999" selected="selected">blabla</option>')
        */
        if ($(e.target).is('option')) { // added an option ?
            var widget = $(e.target).parents('.autocomplete-light-widget');

            if (!widget.length) {
                return;
            }

            widget = widget.yourlabsWidget();
            var option = $(e.target);
            var value = option.attr('value');
            var choice = widget.deck.find('[data-value="'+value+'"]');

            if (!choice.length) {
                var deckChoice = widget.optionChoice(option);

                deckChoice.attr('data-value', value);

                widget.selectChoice(deckChoice);
            }
        } else { // added a widget ?
            var notReady = '.autocomplete-light-widget:not([data-widget-ready])'
            var widget = $(e.target).find(notReady);

            if (!widget.length) {
                return;
            }

            // Ignore inserted autocomplete box elements.
            if (widget.is('.yourlabs-autocomplete')) {
                return;
            }

            // Ensure that the newly added widget is clean, in case it was
            // cloned with data.
            widget.yourlabsWidget('destroy');
            widget.find('input').yourlabsAutocomplete('destroy');

            // added a widget: initialize the widget.
            widget.trigger('initialize');
        }
    });
    
    var ie = yourlabs.getInternetExplorerVersion();
    if (ie != -1 && ie < 9) {
        observe = [
            '.autocomplete-light-widget:not([data-yourlabs-skip])',
            '.autocomplete-light-widget option:not([data-yourlabs-skip])'
        ].join();
        $(observe).attr('data-yourlabs-skip', 1);

        function ieDOMNodeInserted() {
            // http://msdn.microsoft.com/en-us/library/ms536957
            $(observe).each(function() {
                $(document).trigger(jQuery.Event('DOMNodeInserted', {target: $(this)}));
                $(this).attr('data-yourlabs-skip', 1);
            });

            setTimeout(ieDOMNodeInserted, 500);
        }
        setTimeout(ieDOMNodeInserted, 500);
    }

});
