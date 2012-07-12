$(document).ready(function() {
    // get the widget elements
    var countryWidgetElement = $('.autocomplete-light-widget.country');
    var regionWidgetElement = $('.autocomplete-light-widget.region');

    var setupDependantAutocomplete = function() {
        // When the country select changes
        countryWidgetElement.yourlabsWidget().select.bind('change', function() {
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
        });
    }

    // Ensure widgets are ready before calling setupDependantAutocomplete
    countryWidgetElement.data('widget-ready') ? setupDependantAutocomplete() :
        regionWidgetElement.bind('widget-ready', setupDependantAutocomplete);
});
