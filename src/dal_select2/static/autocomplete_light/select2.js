;(function ($) {
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
                $field_selector = '[name=' + prefix + srcName + ']';
                $field = $($field_selector);
                if (!$field.length) {
                    // As a fallback, look for it outside the inline
                    $field_selector = '[name=' + srcName + ']';
                    $field = $($field_selector);
                }
                if ($field.length) {
                    if ($field.attr('type') === 'checkbox')
                        forwardedData[dstName] = $field[0].checked;
                    else if ($field.attr('type') === 'radio')
                        forwardedData[dstName] = $($field_selector + ":checked").val();
                    else
                        forwardedData[dstName] = $field.val();
                }
            }
        });
        return JSON.stringify(forwardedData);
    }

    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function() {
        var element = $(this);

        // Templating helper
        function template(item) {
            if (element.attr('data-html') !== undefined) {
                var $result = $('<span>');
                $result.html(item.text);
                return $result;
            } else {
                return item.text;
            }
        }

        var ajax = null;
        if ($(this).attr('data-autocomplete-light-url')) {
            ajax = {
                url: $(this).attr('data-autocomplete-light-url'),
                dataType: 'json',
                delay: 250,

                data: function (params) {
                    var data = {
                        q: params.term, // search term
                        page: params.page,
                        create: element.attr('data-autocomplete-light-create') && !element.attr('data-tags'),
                        forward: get_forwards(element)
                    };

                    return data;
                },
                processResults: function (data, page) {
                    if (element.attr('data-tags')) {
                        $.each(data.results, function(index, value) {
                            value.id = value.text;
                        });
                    }

                    return data;
                },
                cache: true
            };
        }

        $(this).select2({
            tokenSeparators: element.attr('data-tags') ? [','] : null,
            debug: true,
            placeholder: '',
            minimumInputLength: 0,
            allowClear: ! $(this).is('[required]'),
            templateResult: template,
            templateSelection: template,
            ajax: ajax,
        });

        $(this).on('select2:selecting', function (e) {
            var data = e.params.args.data;

            if (data.create_id !== true)
                return;

            e.preventDefault();

            var select = $(this);

            $.ajax({
                url: $(this).attr('data-autocomplete-light-url'),
                type: 'POST',
                dataType: 'json',
                data: {
                    text: data.id,
                    forward: get_forwards($(this))
                },
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", document.csrftoken);
                },
                success: function(data, textStatus, jqXHR ) {
                    select.append(
                        $('<option>', {value: data.id, text: data.text, selected: true})
                    );
                    select.trigger('change');
                    select.select2('close');
                }
            });
        });

    });
    window.__dal__initListenerIsSet = true;
    $('[data-autocomplete-light-function]:not([id*="__prefix__"])').each(function() {
        window.__dal__initialize(this);
    });

    // Remove this block when this is merged upstream:
    // https://github.com/select2/select2/pull/4249
    $(document).on('DOMSubtreeModified', '[data-autocomplete-light-function=select2] option', function() {
        $(this).parents('select').next().find(
            '.select2-selection--single .select2-selection__rendered'
        ).text($(this).text());
    });
})(yl.jQuery);
