/*
This script garantees that this will be called once in django admin.
However, its the callback's responsability to clean up if the
element was cloned with data - which should be the case.
*/

;(function ($) {
    $.fn.getFormPrefix = function() {
        /* Get the form prefix for a field.
         *
         * For example:
         *
         *     $(':input[name$=owner]').getFormsetPrefix()
         *
         * Would return an empty string for an input with name 'owner' but would return
         * 'inline_model-0-' for an input named 'inline_model-0-owner'.
         */
        var parts = $(this).attr('name').split('-');
        var prefix = '';

        for (var i in parts) {
            var testPrefix = parts.slice(0, -i).join('-');
            if (! testPrefix.length) continue;
            testPrefix += '-';

            var result = $(':input[name^=' + testPrefix + ']')

            if (result.length) {
                return testPrefix;
            }
        }

        return '';
    }

    var initialized = [];

    function initialize(element) {
        if (typeof element === 'undefined' || typeof element === 'number') {
            element = this;
        }

        if (window.__dal__initListenerIsSet !== true || initialized.indexOf(element) >= 0) {
            return;
        }

        $(element).trigger('autocompleteLightInitialize');
        initialized.push(element);
    }
    window.__dal__initialize = initialize;

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
                var cookie = $.trim(cookies[i]);
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
