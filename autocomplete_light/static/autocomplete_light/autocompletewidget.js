function AutocompleteDeck(el, options) {
    this.wrapper = el;
    
    this.options = {
        'input': this.wrapper.find('input[type=text].autocomplete'),
        'valueSelect': this.wrapper.find('select.valueSelect'),
        'channel': $.parseJSON(this.wrapper.find('.json_channel').html()),
        'deck': this.wrapper.find('.deck'),
        'maxItems': this.wrapper.data('maxitems'),
        'getValue': function(deck, result) {
            return $.parseJSON(result.find('textarea').html()).value;
        },
        'selectOption': function(deck, result) {
            var value = deck.options.getValue(deck, result);

            if (deck.options.valueSelect.find('option[value='+value+']').length)
                return; // value already selected

            deck.options.valueSelect.append(
                '<option selected="selected" value="'+ value +'"></option>');

            if (deck.options.maxItems && deck.options.valueSelect.find('option').length > deck.options.maxItems) {
                deck.options.valueSelect.find('option:first').remove();
            }

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
        if (results.length == this.options.maxItems) {
            this.options.input.hide();
        }

        this.options.input.yourlabs_autocomplete({
            url: this.options.channel.url,
            id: this.options.autocompletId,
            iterablesSelector: '.result',
            minCharacters: this.wrapper.data('mincharacters', 0),
        });

        var deck = this;
        $(document).bind('yourlabs_autocomplete.selectOption', function(e, autocomplete, result) {
            if (autocomplete.options.id != deck.options.autocompletId) return;
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
    }
}

$(document).ready(function() {
    $('.autocompleteselectwidget_light').each(function() {
        $(this).yourlabs_deck();
    });
});
