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

    $.fn.getFormPrefixes = function() {
        /*
         * Get the form prefixes for a field, from the most specific to the least.
         *
         * For example:
         *
         *      $(':input[name$=owner]').getFormPrefixes()
         *
         * Would return:
         * - [''] for an input named 'owner'.
         * - ['inline_model-0-', ''] for an input named 'inline_model-0-owner' (i.e. nested with a nested inline).
         * - ['sections-0-items-0-', 'sections-0-', ''] for an input named 'sections-0-items-0-product'
         *   (i.e. nested multiple time with django-nested-admin).
         */
        var parts = $(this).attr('name').split('-').slice(0, -1);
        var prefixes = [];

        for (i = 0; i < parts.length; i += 2) {
            var testPrefix = parts.slice(0, -i || parts.length).join('-');
            if (!testPrefix.length)
                continue;

            testPrefix += '-';

            var result = $(':input[name^=' + testPrefix + ']')

            if (result.length)
                prefixes.push(testPrefix);
        }

        prefixes.push('');

        return prefixes;
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

    if (!window.__dal__initialize) {
        window.__dal__initialize = initialize;

        $(document).ready(function () {
            $('[data-autocomplete-light-function=select2]:not([id*="__prefix__"])').each(initialize);
        });

        $(document).bind('DOMNodeInserted', function (e) {
            $(e.target).find('[data-autocomplete-light-function=select2]').each(initialize);
        });
    }

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
    if (document.csrftoken === null) {
        // Try to get CSRF token from DOM when cookie is missing
        var $csrf = $('form :input[name="csrfmiddlewaretoken"]');
        if ($csrf.length > 0) {
            document.csrftoken = $csrf[0].value;
        }
    }
})(yl.jQuery);

// Does the same thing as django's admin/js/autocomplete.js, but uses yl.jQuery.
(function($) {
    'use strict';
    var init = function($element, options) {
        var settings = $.extend({
            ajax: {
                data: function(params) {
                    return {
                        term: params.term,
                        page: params.page
                    };
                }
            }
        }, options);
        $element.select2(settings);
    };

    $.fn.djangoAdminSelect2 = function(options) {
        var settings = $.extend({}, options);
        $.each(this, function(i, element) {
            var $element = $(element);
            init($element, settings);
        });
        return this;
    };

    $(function() {
        // Initialize all autocomplete widgets except the one in the template
        // form used when a new formset is added.
        $('.admin-autocomplete').not('[name*=__prefix__]').djangoAdminSelect2();
    });

    $(document).on('formset:added', (function() {
        return function(event, $newFormset) {
            return $newFormset.find('.admin-autocomplete').djangoAdminSelect2();
        };
    })(this));
}(yl.jQuery));
