$(document).ready(function() {
    $('.autocomplete-light-widget select[name$=country]').live('change', function() {
        var countrySelectElement = $(this);
        var countryWidgetElement = $(this).parents('.autocomplete-light-widget');
        var regionSelectElement = $('#' + $(this).attr('id').replace('country', 'region'));
        var regionWidgetElement = regionSelectElement.parents('.autocomplete-light-widget');

        // When the country select changes
        value = $(this).val();

        if (value) {
            // If value is contains something, add it to autocomplete.data
            regionWidgetElement.yourlabsWidget().autocomplete.data = {
                'country_id': value[0],
            };
        } else {
            // If value is empty, empty autocomplete.data
            regionWidgetElement.yourlabsWidget().autocomplete.data = {}
        }

        // example debug statements, that does not replace using breakbpoints and a proper debugger but can hel
        // console.log($(this), 'changed to', value);
        // console.log(regionWidgetElement, 'data is', regionWidgetElement.yourlabsWidget().autocomplete.data)
    })
});
