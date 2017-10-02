;(function ($) {
    /*
     * This purpose of this script isn't to initialize the field but rather cause some side effect
     * so the tests can verify whether this has been run.
     * This purpose of this script isn't to initialize the field but rather cause some side effect
     * so the tests can verify whether this has been run.
     */
    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=tSelect2]', function() {
        window.__dal__tSelect2Initialized = true;
    });
    window.__dal__tSelect2Setup = true;
})(yl.jQuery);
