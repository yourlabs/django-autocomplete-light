/*
 * The purpose of this script isn't to initialize the field but rather cause some side effect
 * so the tests can verify whether this has been run.
 */

// New Method
document.addEventListener('dal-init-function', function () {
    yl.registerFunction( 'tSelect2', function ($, element) {
        window.__dal__tSelect2Initialized = true;
    });
    window.__dal__tSelect2Setup = true;
});

// Deprecated method
window.onload = function() {
    (function ($) {
        $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=tSelect2]', function () {
            window.__dal__tSelect2Initialized_depricated = true;
        });
        window.__dal__tSelect2Setup_depricated = true;
    })(django.jQuery);
}
