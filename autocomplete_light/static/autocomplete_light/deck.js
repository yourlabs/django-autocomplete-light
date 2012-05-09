function AutocompleteDeck(el) {
    this.wrapper = el;
    
    this.input = this.wrapper.find('input[type=text].autocomplete')
    this.valueSelect = this.wrapper.find('select.valueSelect');
    this.channel = $.parseJSON(this.wrapper.find('.json_channel').html());
    this.deck = this.wrapper.find('.deck');
    this.addTemplate = this.wrapper.find('.add_template .result');
    this.maxItems = this.wrapper.data('maxitems');
    this.getValue = function(result) {
        return result.data('value');
    };
    this.initializeAutocomplete = function() {
        this.input.yourlabs_autocomplete(this.autocompleteOptions);
    };
    this.bindSelectOption = function() {
        this.input.bind('selectOption', function(e, option) {
            var wrapper = $(this).parents('.autocomplete_light_widget');
            var deck = wrapper.yourlabs_deck();
            deck.selectOption(option);
        });
    };
    this.selectOption = function(result, force) {
        var value = this.getValue(result);

        if (this.valueSelect.find('option[value='+value+']').length && !force)
            return; // value already selected and force is not on

        this.valueSelect.append(
            '<option selected="selected" value="'+ value +'"></option>');

        if (this.maxItems && this.valueSelect.find('option').length > this.maxItems) {
            var remove_option = this.valueSelect.find('option:first');
            var remove_value = remove_option.attr('value');
            this.deck.find('.result[data-value='+remove_value+']').remove();
            remove_option.remove();
        }
        this.valueSelect.trigger('change');

        if (this.maxItems && this.valueSelect.find('option').length == this.maxItems) {
            this.input.hide();
            this.input.val('');
        }

        var result = result.clone();
        this.deck.append(result);
        result.append('<span class="remove">' + this.wrapper.find('.remove').html() + '</span>');
        this.deck.show();
    }
    this.deselectOption = function(result) {
        var value = this.getValue(result);

        this.valueSelect.find('option[value='+value+']').remove();
        this.valueSelect.trigger('change');
        result.remove();

        if (this.deck.find('*').length == 0) {
            this.deck.hide();
        }

        if (this.maxItems && this.valueSelect.find('option').length < this.maxItems) {
            this.input.show();
        }
    };
    this.autocompletId = this.input.attr('id');
    this.autocompleteOptions = {
        url: this.channel.url,
        id: this.autocompletId,
        iterablesSelector: '.result',
        minCharacters: this.wrapper.data('mincharacters', 0),
        outerContainerClasses: 'autocomplete_light_widget',
    }
    this.initialize = function() {
        var results = this.deck.find('.result');

        results.append(this.wrapper.find('.remove:last').clone().show());
        if (this.maxItems > 0 && results.length == this.maxItems) {
            this.input.hide();
        }

        this.initializeAutocomplete();
        this.bindSelectOption();
    }
}

$.fn.yourlabs_deck = function(overrides) {
    var id;
    overrides = overrides ? overrides : {};
    id = overrides.id || this.attr('id');

    if (!(id && this)) {
        alert('failure: the element needs an id attribute, or an id option must be passed');
        return false;
    }

    if ($.fn.yourlabs_deck.registry == undefined) {
        $.fn.yourlabs_deck.registry = {};
    }
    
    if ($.fn.yourlabs_deck.registry[id] == undefined) {
        $.fn.yourlabs_deck.registry[id] = new AutocompleteDeck(this);
        $.fn.yourlabs_deck.registry[id] = $.extend($.fn.yourlabs_deck.registry[id], overrides);
        $.fn.yourlabs_deck.registry[id].initialize();
        $.fn.yourlabs_deck.registry[id].wrapper.attr('data-deckready', 1);
        $.fn.yourlabs_deck.registry[id].wrapper.trigger('deckready');
    }

    return $.fn.yourlabs_deck.registry[id];
}

$(document).ready(function() {
    $('.autocomplete_light_widget[data-bootstrap=normal]').each(function() {
        var deck = $(this).yourlabs_deck();
    });

    $('.autocomplete_light_widget .deck .remove').live('click', function() {
        var wrapper = $(this).parents('.autocomplete_light_widget');
        if (!wrapper.length) return;
        var deck = wrapper.yourlabs_deck();
        var selector = deck.input.yourlabs_autocomplete().iterablesSelector;
        var result = $(this).parents(selector);
        deck.deselectOption(result);
    });

    // support values added directly in the select via js (ie. admin + sign)
    // for this, we make one timer that regularely checks for values in the select
    // that are not in the deck. The reason for that is that change is not triggered
    // when options are added like this:
    // $('select#id_dependencies').append(
    //      '<option value="9999" selected="selected">blabla</option>')
    function updateDecks() {
        $('.autocomplete_light_widget[data-deckready=1]').each(function() {
            var deck = $(this).yourlabs_deck();
            var value = deck.valueSelect.val();

            function updateValueDisplay(value) {
                if (!value) return;

                var result = deck.deck.find('.result[data-value='+value+']');
                if (!result.length) {
                    var result = deck.addTemplate.clone();
                    var html = deck.valueSelect.find('option[value='+value+']').html();
                    result.html(html);
                    result.attr('data-value', value);
                    deck.selectOption(result, true);
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
