;(function ($) {
    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function() {
        var element = $(this);

        // This widget has a clear button
        $(this).find('option[value=""]').remove();

        $(this).select2({
            tags: element.attr('data-tags'),
            debug: true,
            placeholder: '',
            minimumInputLength: 0,
            allowClear: ! $(this).is('required'),
            ajax: {
                url: $(this).attr('data-autocomplete-light-url'),
                dataType: 'json',
                delay: 250,

                data: function (params) {
                    var data = {
                        q: params.term, // search term
                        page: params.page,
                        create: element.attr('data-autocomplete-light-create') && !element.attr('data-tags'),
                    };

                    var forward = element.attr('data-autocomplete-light-forward');
                    if (forward !== undefined) {
                        var data_forward = {};
                        forward = forward.split(',');

                        for (var key in forward) {
                            data_forward[forward[key]] = $('[name=' + forward[key] + ']').val();
                        }

                        data.forward = JSON.stringify(data_forward);
                    }

                    return data;
                },
                processResults: function (data, page) {
                    return {
                        results: data.results,
                        pagination: {
                            more: data.more
                        }
                    };
                },
                cache: true
            },
        });
    });

    $(document).on('DOMSubtreeModified', '[data-autocomplete-light-function=select2] option', function() {
        var id = $(this).parents('select').attr('id')
        var newText = $(this).text()
        $('#select2-' + id + '-container').text(newText);
    });
})(yl.jQuery);
