var yl = yl || {};
if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
    // If django.jQuery is already defined, use it.
    yl.jQuery = django.jQuery;
}
else {
    // We include jquery itself in our widget's media, because we need it.
    // Normally, we expect our widget's reference to admin/js/vendor/jquery/jquery.js
    // to be skipped, because django's own code has already included it.
    // However, if django.jQuery is NOT defined, we know that jquery was not
    // included before we did it ourselves. This can happen if we're not being
    // rendered in a django admin form.
    // However, someone ELSE'S jQuery may have been included before ours, in
    // which case we must ensure that our jquery doesn't override theirs, since
    // it might be a newer version that other code on the page relies on.
    // Thus, we must run jQuery.noConflict(true) here to move our jQuery out of
    // the way.
    yl.jQuery = jQuery.noConflict(true);
}

// In addition to all of this, we must ensure that the global jQuery and $ are
// defined, because Select2 requires that. jQuery will only be undefined at
// this point if only we or django included it.
if (typeof jQuery === 'undefined') {
    jQuery = yl.jQuery;
    $ = yl.jQuery;
}
else {
    // jQuery IS still defined, which means someone else also included jQuery.
    // In this situation, we need to store the old jQuery in a
    // temp variable, set the global jQuery to our yl.jQuery, then let select2
    // set itself up. We restore the global jQuery to its original value in
    // jquery.post-setup.js.
    dal_jquery_backup = jQuery.noConflict(true);
    jQuery = yl.jQuery;
}
