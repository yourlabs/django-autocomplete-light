function AutocompleteDeck(el, options) {
    this.wrapper = el;
    
    this.options = {
        'input': this.wrapper.find('input[type=text].autocomplete'),
        'valueSelect': this.wrapper.find('select.valueSelect'),
        'channel': $.parseJSON(this.wrapper.find('.json_channel').html()),
        'deck': this.wrapper.find('.deck'),
        'addTemplate': this.wrapper.find('.add_template .result'),
        'maxItems': this.wrapper.data('maxitems'),
        'getValue': function(deck, result) {
            return result.data('value');
        },
        'selectOption': function(deck, result, force) {
            var value = deck.options.getValue(deck, result);

            if (deck.options.valueSelect.find('option[value='+value+']').length && !force)
                return; // value already selected and force is not on

            deck.options.valueSelect.append(
                '<option selected="selected" value="'+ value +'"></option>');

            if (deck.options.maxItems && deck.options.valueSelect.find('option').length > deck.options.maxItems) {
                var remove_option = deck.options.valueSelect.find('option:first');
                var remove_value = remove_option.attr('value');
                deck.options.deck.find('.result[data-value='+remove_value+']').remove();
                remove_option.remove();
            }
            deck.options.valueSelect.trigger('change');

            if (deck.options.maxItems && deck.options.valueSelect.find('option').length == deck.options.maxItems) {
                deck.options.input.hide();
                deck.options.input.val('');
            }

            var result = result.clone();
            deck.options.deck.append(result);
            result.append('<span class="remove">' + deck.wrapper.find('.remove').html() + '</span>');
            deck.options.deck.show();
        },
        'deselectOption': function(deck, result) {
            var value = deck.options.getValue(deck, result);

            deck.options.valueSelect.find('option[value='+value+']').remove();
            deck.options.valueSelect.trigger('change');
            result.remove();

            if (deck.options.deck.find('*').length == 0) {
                deck.options.deck.hide();
            }

            if (deck.options.maxItems && deck.options.valueSelect.find('option').length < deck.options.maxItems) {
                deck.options.input.show();
            }
        },
    }
    this.options['autocompletId'] = this.options.input.attr('id');
    this.options = $.extend(this.options, options);
    this.initialize();
}

$.fn.yourlabs_deck = function(options) {
    var id;
    options = options ? options : {};
    id = options.id || this.attr('id');

    if (!(id && this)) {
        alert('failure: the element needs an id attribute, or an id option must be passed');
        return false;
    }

    if ($.fn.yourlabs_deck.registry == undefined) {
        $.fn.yourlabs_deck.registry = {};
    }
    
    if ($.fn.yourlabs_deck.registry[id] == undefined) {
        $.fn.yourlabs_deck.registry[id] = new AutocompleteDeck(this, options);
    }

    return $.fn.yourlabs_deck.registry[id];
}

AutocompleteDeck.prototype = {
    initialize: function() {
        var results = this.options.deck.find('.result');

        results.append(this.wrapper.find('.remove:last').clone().show());
        if (this.options.maxItems > 0 && results.length == this.options.maxItems) {
            this.options.input.hide();
        }

        this.options.input.yourlabs_autocomplete({
            url: this.options.channel.url,
            id: this.options.autocompletId,
            iterablesSelector: '.result',
            minCharacters: this.wrapper.data('mincharacters', 0),
        });

        this.wrapper.attr('data-ready', '1');
    }
}

$(document).ready(function() {
    $('.autocompleteselectwidget_light[data-bootstrap=normal]').each(function() {
        $(this).yourlabs_deck();
    });

    $(document).bind('yourlabs_autocomplete.selectOption', function(e, autocomplete, result) {
        var wrapper = autocomplete.el.parents('.autocompleteselectwidget_light');
        var deck = wrapper.yourlabs_deck();
        deck.options.selectOption(deck, result);
    });

    $('.autocompleteselectwidget_light .deck .remove').live('click', function() {
        var wrapper = $(this).parents('.autocompleteselectwidget_light');
        if (!wrapper.length) return;
        var deck = wrapper.yourlabs_deck();
        var selector = deck.options.input.yourlabs_autocomplete().options.iterablesSelector;
        var result = $(this).parents(selector);
        deck.options.deselectOption(deck, result);
    });

    // support values added directly in the select via js (ie. admin + sign)
    // for this, we make one timer that regularely checks for values in the select
    // that are not in the deck. The reason for that is that change is not triggered
    // when options are added like this:
    // $('select#id_dependencies').append(
    //      '<option value="9999" selected="selected">blabla</option>')
    function updateDecks() {
        $('.autocompleteselectwidget_light[data-ready=1]').each(function() {
            var deck = $(this).yourlabs_deck();
            var value = deck.options.valueSelect.val();

            function updateValueDisplay(value) {
                if (!value) return;

                var result = deck.options.deck.find('.result[data-value='+value+']');
                if (!result.length) {
                    var result = deck.options.addTemplate.clone();
                    var html = deck.options.valueSelect.find('option[value='+value+']').html();
                    result.html(html);
                    result.attr('data-value', value);
                    deck.options.selectOption(deck, result, true);
                }
            }

            if (value instanceof Array) {
                for(var i=0; i<value.length; i++) {
                    updateValueDisplay(value[i]);
                }
            } else {
                updateValueDisplay(value);
            }
        });
        setTimeout(updateDecks, 2000);
    }
    setTimeout(updateDecks, 1000);
});
