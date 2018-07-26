import $ from 'jquery'

$(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function() {
    var element = $(this);

    // Templating helper
    function template(text, is_html) {
        if (is_html) {
            var $result = $('<span>');
            $result.html(text);
            return $result;
        }
        return text;

    }

    function result_template(item) {
        return template(
            item.text,
            element.attr('data-html') !== undefined || element.attr('data-result-html') !== undefined
        );
    }

    function selected_template(item) {
        if (item.selected_text !== undefined) {
            return template(
                item.selected_text,
                element.attr('data-html') !== undefined || element.attr('data-selected-html') !== undefined
            );
        }
        return result_template(item);


    }

    var ajax = null;
    if ($(this).attr('data-autocomplete-light-url')) {
        ajax = {
            'url': $(this).attr('data-autocomplete-light-url'),
            'dataType': 'json',
            'delay': 250,

            'data' (params) {
                var data = {
                    'q': params.term, // search term
                    'page': params.page,
                    'create': element.attr('data-autocomplete-light-create') && !element.attr('data-tags'),
                    'forward': getForwards(element)
                };

                return data;
            },
            'processResults' (data, page) {
                if (element.attr('data-tags')) {
                    $.each(data.results, function(index, value) {
                        value.id = value.text;
                    });
                }

                return data;
            },
            'cache': true
        };
    }

    $(this).select2({
        'tokenSeparators': element.attr('data-tags') ? [','] : null,
        'debug': true,
        'placeholder': '',
        'language': element.attr('data-autocomplete-light-language'),
        'minimumInputLength': 0,
        'allowClear': ! $(this).is('[required]'),
        'templateResult': result_template,
        'templateSelection': selected_template,
        ajax,
        'tags': Boolean(element.attr('data-tags'))
    });

    $(this).on('select2:selecting', function (e) {
        var data = e.params.args.data;

        if (data.create_id !== true)
            return;

        e.preventDefault();

        var select = $(this);

        $.ajax({
            'url': $(this).attr('data-autocomplete-light-url'),
            'type': 'POST',
            'dataType': 'json',
            'data': {
                'text': data.id,
                'forward': getForwards($(this))
            },
            'beforeSend'(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', document.csrftoken);
            },
            'success'(data, textStatus, jqXHR) {
                select.append($('<option>', {'value': data.id,
                    'text': data.text,
                    'selected': true}));
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
