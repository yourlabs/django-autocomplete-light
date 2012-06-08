var RemoteChannelDeck = {
    // The default deck getValue() implementation just returns the PK from the
    // result HTML. RemoteChannelDeck's implementation checks for a textarea
    // that would contain a JSON dict in the result's HTML. If the dict has a
    // 'value' key, then return this value. Otherwise, make a blocking ajax
    // request: POST the json dict to the channel url. It expects that the
    // response will contain the value.
    getValue: function(result) {
        var json = result.find('textarea').html();
        var data = $.parseJSON(json);

        var value = false;

        if (data.value) {
            value = data.value;
        } else {
            $.ajax(this.payload.channel.url, {
                async: false,
                type: 'post',
                data: {
                    'result': json,
                },
                success: function(text, jqXHR, textStatus) {
                    value = text;
                }
            });
        }

        return value;
    }
}

$(document).ready(function() {
    // Instanciate decks with RemoteChannelDeck as override for all widgets with
    // channel 'remote'.
    $('.autocomplete_light_widget[data-bootstrap=remote]').each(function() {
        $(this).yourlabs_deck(RemoteChannelDeck);
    });
});
