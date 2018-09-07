var yl = yl || {};
// Directly above this file, we included the jQuery provided by django. That
// means it set itself to window.$ and window.jQuery, and stored away any
// existing jQuery that may have been installed previously. Calling
// jQuery.noConflict(true) will remove OUR copy of jQuery from the global
// namespace and restore the original values of window.$ and window.jQuery.
// This is necessary so that code which uses a version of jQuery that may
// have been installed up-page gets the version it expects.
yl.jQuery = jQuery.noConflict(true);

// Here, we set up django.jQuery, instead of letting admin/js/jquery.init.js
// do it. This is necessary because it ALSO calls jQuery.noConflict(true).
// It we let it do that, it would break any code further down the page that
// expects window.$ and window.jQuery to be defined.
var django = django || {};
if (typeof django.jQuery === 'undefined') {
    // If django.jQuery is not yet defined, we need to define it so that
    // admin/js/autocomplete.js (which we include with our widget) can run.
    django.jQuery = yl.jQuery;
}
