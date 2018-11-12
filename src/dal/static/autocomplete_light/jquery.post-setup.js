if (typeof dal_jquery_backup !== 'undefined') {
    // We made a backup of the original global jQuery before forcing it to our
    // yl.jQuery value. Now that select2 has been set up, we need to restore
    // our backup to its rightful place.
    jQuery = dal_jquery_backup;
    $ = dal_jquery_backup;
}
