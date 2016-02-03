/*
This script garantees that this will be called once in django admin.
However, its the callback's responsability to clean up if the
element was cloned with data - which should be the case.
*/

;(function ($) {
    var initialized = [];

    function initialize() {
        var element = $(this).get(0);

        if (initialized.indexOf(element) >= 0) {
            return
        }

        $(this).trigger('autocompleteLightInitialize');
        initialized.push(element);
    }

    $(document).ready(function() {
        $('[data-autocomplete-light-function]:not([id*="__prefix__"])').each(initialize);
    });

    $(document).bind('DOMNodeInserted', function(e) {
        $(e.target).find('[data-autocomplete-light-function]').each(initialize);
    });
})(yl.jQuery);
