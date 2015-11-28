OnTheFlyWidget = {
    getValue: function(choice) {
        var value = choice.data('value');

        if (value == 'create') {
            choice.html(this.input.val())

            $.ajax(this.autocomplete.url, {
                async: false,
                type: 'post',
                data: {
                    'name': this.input.val(),
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
    $('body').on('initialize', '.autocomplete-light-widget[data-widget-bootstrap=onthefly-widget]', function() {
        $(this).yourlabsWidget(OnTheFlyWidget);
    });
});
