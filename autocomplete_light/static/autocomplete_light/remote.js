if (window.yourlabs == undefined) window.yourlabs = {};

yourlabs.RemoteAutocompleteWidget = {
    /*
    The default deck getValue() implementation just returns the PK from the
    choice HTML. RemoteAutocompleteWidget.getValue's implementation checks for
    a url too. If a url is found, it will post to that url and expect the pk to
    be in the response.

    This is how autocomplete-light supports proposing values that are not there
    in the database until user selection.
    */
    getValue: function(choice) {
        var value = choice.data('value');

        if (typeof(value)=='string' && isNaN(value) && value.match(/^https?:/)) {
            $.ajax(this.autocompleteOptions.url, {
                async: false,
                type: 'post',
                data: {
                    'value': value
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

$(document).bind('yourlabsWidgetReady', function() {
    // Instanciate decks with RemoteAutocompleteWidget as override for all widgets with
    // autocomplete 'remote'.
    $('body').on('initialize', '.autocomplete-light-widget[data-bootstrap=rest_model]', function() {
        $(this).yourlabsWidget(yourlabs.RemoteAutocompleteWidget);
    });
});
