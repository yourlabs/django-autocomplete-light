;(function ($) {
    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=jal]', function() {
        $(this).yourlabsWidget();
    });
    window.__dal__initListenerIsSet = true;
    $('[data-autocomplete-light-function=jal]:not([id*="__prefix__"])').each(function() {
        window.__dal__initialize(this);
    });
})(yl.jQuery);
