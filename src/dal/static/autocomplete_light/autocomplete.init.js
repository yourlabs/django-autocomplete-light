/*
This script garantees that this will be called once in django admin.
However, its the callback's responsability to clean up if the
element was cloned with data - which should be the case.
*/

;(function ($) {
    var initialized = [];

    function initialize() {
        var element = $(this).get(0);

        if (initialized.indexOf(element) >= 0) {
            return
        }

        $(this).trigger('autocompleteLightInitialize');
        initialized.push(element);
    }

    $(document).ready(function() {
        $('[data-autocomplete-light-function]:not([id*="__prefix__"])').each(initialize);
    });

    $(document).bind('DOMNodeInserted', function(e) {
        $(e.target).find('[data-autocomplete-light-function]').each(initialize);
    });

    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    document.csrftoken = getCookie('csrftoken');
})(yl.jQuery);
