;(function ($) {
    function add_forwards(element) {
        var forward = element.attr('data-autocomplete-light-forward');
        if (forward !== undefined) {
            forward = forward.split(',');

            var prefix = $(element).getFormPrefix();
            var data_forward = {};

            for (var key in forward) {
                // First look for this field in the inline
                var $field = $('[name=' + prefix + forward[key] + ']');
                if (!$field.length)
                    // As a fallback, look for it outside the inline
                    $field = $('[name=' + forward[key] + ']');
                if ($field.length)
                    data_forward[forward[key]] = $field.val();
            }

            return JSON.stringify(data_forward);
        }
    }

    function clear_select2(element) {
        element.find("option").remove();
        $(element).val(null).trigger('change');
    }

    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function() {
        var element = $(this);

        // This widget has a clear button
        $(this).find('option[value=""]').remove();

        // Templating helper
        function template(item) {
            if (element.attr('data-html')) {
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
                        forward: add_forwards(element)
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
            allowClear: ! $(this).is('required'),
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
                    forward: add_forwards($(this))
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

    $(document).on('change', '[data-autocomplete-light-forward-feedback]', function() {
        var prefix = $(this).getFormPrefix();
        var feedback = $(this).data("autocomplete-light-forward-feedback");
        var feedback_splitted;

        if ($.inArray("suppressFeedback", arguments) != -1) {
            return;
        }
        if (feedback) {
            feedback_splitted = feedback.split(",");
        } else {
            feedback_splitted = [];
        }
        $.each(feedback_splitted, function(ix, fb) {
            var sel_type;
            var sel_equals;
            var name;
            var name_with_prefix;
            var to_clear;

            if (fb.length === 0) {
                return;
            }

            sel_type = fb[0];

            if (sel_type === "$") {
                sel_equals = "$=";
                name = fb.slice(1);
            } else if (sel_type === "^") {
                sel_equals = "^=";
                name = fb.slice(1);
            } else if (sel_type === "*") {
                sel_equals = "*=";
                name = fb.slice(1);
            } else {
                sel_equals = "=";
                name = fb;
            }

            name_with_prefix = prefix + name;

            to_clear = $('[name' + sel_equals + name_with_prefix + ']');

            if (to_clear.length === 0) {
                to_clear = $('[name' + sel_equals + name + ']');
            }

            to_clear.each(function(ix, el) {
                clear_select2(to_clear);
            });

        });
    });

    // Remove this block when this is merged upstream:
    // https://github.com/select2/select2/pull/4249
    $(document).on('DOMSubtreeModified', '[data-autocomplete-light-function=select2] option', function() {
        $(this).parents('select').next().find(
            '.select2-selection--single .select2-selection__rendered'
        ).text($(this).text());
    });
})(yl.jQuery);
