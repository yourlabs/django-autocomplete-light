var yl = yl || {};

if (yl.jQuery === undefined) {
    if (django.jQuery !== undefined)
        yl.jQuery = django.jQuery

    else if (typeof $ !== 'undefined')
        yl.jQuery = $;
}
