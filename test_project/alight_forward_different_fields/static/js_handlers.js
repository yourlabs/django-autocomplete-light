$(document).ready(function() {
    yl.registerForwardHandler("const42", function () {
        return 42;
    });

    yl.registerForwardHandler("reverse_name", function(elem) {
        var field = yl.getFieldRelativeTo(elem, "name");

        var name = field.val();
        return name.split("").reverse().join("");
    });
});