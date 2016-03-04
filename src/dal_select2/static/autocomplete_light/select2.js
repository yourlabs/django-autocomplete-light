;(function ($) {
    $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function() {
        var element = $(this);

        // This widget has a clear button
        $(this).find('option[value=""]').remove();

        $(this).select2({
            tokenSeparators: element.attr('data-tags') ? [','] : null,
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
                    if (element.attr('data-tags')) {
                        $.each(data.results, function(index, value) {
                            value.id = value.text;
                        });
                    }

                    return data;
                },
                cache: true
            },
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

    $(document).on('DOMSubtreeModified', '[data-autocomplete-light-function=select2] option', function() {
        var id = $(this).parents('select').attr('id')
        var newText = $(this).text()
        $('#select2-' + id + '-container').text(newText);
    });
})(yl.jQuery);
