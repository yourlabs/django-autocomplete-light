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

        prefixes = $(element).getFormPrefixes();
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
                for (var i = 0; i < prefixes.length; i++) {
                    $field_selector = '[name=' + prefixes[i] + srcName + ']';
                    $field = $($field_selector);

                    if ($field.length) {
                        if ($field.length) {
                            if ($field.attr('type') === 'checkbox')
                                forwardedData[dstName] = $field[0].checked;
                            else if ($field.attr('type') === 'radio')
                                forwardedData[dstName] = $($field_selector + ":checked").val();
                            else
                                forwardedData[dstName] = $field.val();
                        }

                        break;  // break after first match
                    }
                }
            }
        });
        return JSON.stringify(forwardedData);
    }

    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function() {
        var element = $(this);

        // Templating helper
        function template(text, is_html) {
            if (is_html) {
                var $result = $('<span>');
                $result.html(text);
                return $result;
            } else {
                return text;
            }
        }

        function result_template(item) {
            return template(item.text,
                element.attr('data-html') !== undefined || element.attr('data-result-html') !== undefined
            );
        }

        function selected_template(item) {
            if (item.selected_text !== undefined) {
                return template(item.selected_text,
                    element.attr('data-html') !== undefined || element.attr('data-selected-html') !== undefined
                );
            } else {
                return result_template(item);
            }
            return
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
            language: element.attr('data-autocomplete-light-language'),
            minimumInputLength: 0,
            allowClear: ! $(this).is('[required]'),
            templateResult: result_template,
            templateSelection: selected_template,
            ajax: ajax,
            tags: Boolean(element.attr('data-tags')),
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
    $('[data-autocomplete-light-function=select2]:not([id*="__prefix__"])').each(function() {
        window.__dal__initialize(this);
    });
})(yl.jQuery);
