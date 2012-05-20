var GenericChannelDeck = {
    getValue: function(result) {
        var data = $.parseJSON(result.find('textarea').html());
        return data.content_type + ';' + data.object_id;
    },
    selectOption: function(result) {
        // Get the unique value for this result.
        var value = this.getValue(result);

        // Parse data for this result.
        var data = $.parseJSON(result.find('textarea').html());

        // Find the content type field for this generic relation.
        var content_type_field = $('#id_' +
            this.payload.content_type_field_name);
        // Set the value of this field.
        content_type_field.val(data.content_type);
        content_type_field.trigger('change');

        // Set the object_id field value.
        this.valueSelect.val(data.object_id);
        this.valueSelect.trigger('change');
    }
}

// Instanciate decks with GenericChannelDeck as override for all widgets with
// channel 'generic'.
$('.autocomplete_light_widget[data-bootstrap=generic]').each(function() {
    $(this).yourlabs_deck(GenericChannelDeck);
});
