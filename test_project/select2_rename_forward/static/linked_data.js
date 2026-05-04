$(document).ready(function() {
    $(':input[name$=owner]').on('change', function() {
        var prefix = $(this).getFormPrefix();
        $(':input[name=' + prefix + 'test]').val(null).trigger('change');
    });
});
