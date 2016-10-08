function get_forwards(element) {
    var forwardElem, forwardList, prefix, forwardedData, divSelector, form;
    divSelector = "div.dal-forward-conf#dal-forward-conf-for-" +
            element.attr("id");
    form = element.length > 0 ? $(element[0].form) : $();

    forwardElem =
        form.find(divSelector).find('script');
    if (forwardElem.length === 0) {
        return;
    }
    try {
        forwardList = JSON.parse(forwardElem.text());
    } catch (e) {
        return;
    }

    if (!Array.isArray(forwardList)) {
        return;
    }

    prefix = $(element).getFormPrefix();
    forwardedData = {};

    $.each(forwardList, function(ix, f) {
        if (f["type"] === "const") {
            forwardedData[f["dst"]] = f["val"];
        } else if (f["type"] === "field") {
            var srcName, dstName;
            srcName = f["src"];
            if (f.hasOwnProperty("dst")) {
                dstName = f["dst"];
            } else {
                dstName = srcName;
            }
            // First look for this field in the inline
            $field = $('[name=' + prefix + srcName + ']');
            if (!$field.length)
                // As a fallback, look for it outside the inline
                $field = $('[name=' + srcName + ']');
            if ($field.length)
                forwardedData[dstName] = $field.val();

        }
    });
    return JSON.stringify(forwardedData);
}