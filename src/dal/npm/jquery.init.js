var yl = yl || {};

if (yl.jQuery === undefined) {
    /* If the user has included another copy of jQuery use that, even in the admin */
    if (typeof $ !== 'undefined')
        yl.jQuery = $;
    else if ((typeof django !== 'undefined') && (typeof django.jQuery !== 'undefined'))
        yl.jQuery = django.jQuery;
}
