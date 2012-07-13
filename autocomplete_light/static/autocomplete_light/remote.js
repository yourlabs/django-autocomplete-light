var RemoteAutocompleteWidget = {
    /*
    The default deck getValue() implementation just returns the PK from the
    choice HTML. RemoteAutocompleteWidget's implementation checks for a textarea
    that would contain a JSON dict in the choice's HTML. If the dict has a
    'value' key, then return this value. Otherwise, make a blocking ajax
    request: POST the json dict to the autocomplete url. It expects that the
    response will contain the value.
    */
    getValue: function(choice) {
        var value = choice.data('value');

        if (typeof(value)=='string' && isNaN(value) && value.match(/^http:/)) {
            $.ajax(this.autocompleteOptions.url, {
                async: false,
                type: 'post',
                data: {
                    'value': value,
                },
                success: function(text, jqXHR, textStatus) {
                    value = text;
                }
            });

            choice.data('value', value);
        }

        return value;
    }
}

$(document).ready(function() {
    // Instanciate decks with RemoteAutocompleteWidget as override for all widgets with
    // autocomplete 'remote'.
    $('.autocomplete-light-widget[data-bootstrap=rest_model]').each(function() {
        $(this).yourlabsWidget(RemoteAutocompleteWidget);
    });
});
