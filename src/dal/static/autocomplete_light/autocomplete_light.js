window.addEventListener("load", function () {

    var yl = yl || {};

    (function ($) {
        $.fn.getFormPrefix = function () {
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
                if (!testPrefix.length) continue;
                testPrefix += '-';

                var result = $(':input[name^=' + testPrefix + ']')

                if (result.length) {
                    return testPrefix;
                }
            }

            return '';
        }

        $.fn.getFormPrefixes = function () {
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

        /*
         * This ensures the Language file is loaded and passes it our jQuery.
         */
        if (typeof dalLoadLanguage !== 'undefined') {
            dalLoadLanguage($);
        } else {
            document.addEventListener('dal-language-loaded', function (e) {
                // `e.lang` is the language that was loaded.
                dalLoadLanguage($);
            })
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

            if ('MutationObserver' in window) {
                new MutationObserver(function (mutations) {
                    var mutationRecord;
                    var addedNode;

                    for (var i = 0; i < mutations.length; i++) {
                        mutationRecord = mutations[i];

                        if (mutationRecord.addedNodes.length > 0) {
                            for (var j = 0; j < mutationRecord.addedNodes.length; j++) {
                                addedNode = mutationRecord.addedNodes[j];

                                $(addedNode).find('[data-autocomplete-light-function=select2]').each(initialize);
                            }
                        }
                    }

                }).observe(document.documentElement, {childList: true, subtree: true});
            } else {
                $(document).on('DOMNodeInserted', function (e) {
                    $(e.target).find('[data-autocomplete-light-function=select2]').each(initialize);
                });
            }
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
    })(django.jQuery);

// Does the same thing as django's admin/js/autocomplete.js, but uses yl.jQuery.
    (function ($) {
        'use strict';
        var init = function ($element, options) {
            var settings = $.extend({
                ajax: {
                    data: function (params) {
                        return {
                            term: params.term,
                            page: params.page
                        };
                    }
                }
            }, options);
            $element.select2(settings);
        };

        $.fn.djangoAdminSelect2 = function (options) {
            var settings = $.extend({}, options);
            $.each(this, function (i, element) {
                var $element = $(element);
                init($element, settings);
            });
            return this;
        };

        $(function () {
            // Initialize all autocomplete widgets except the one in the template
            // form used when a new formset is added.
            $('.admin-autocomplete').not('[name*=__prefix__]').djangoAdminSelect2();
        });

        $(document).on('formset:added', (function () {
            return function (event, $newFormset) {
                return $newFormset.find('.admin-autocomplete').djangoAdminSelect2();
            };
        })(this));
    }(django.jQuery));

    (function ($, yl) {
        yl.forwardHandlerRegistry = yl.forwardHandlerRegistry || {};

        yl.registerForwardHandler = function (name, handler) {
            yl.forwardHandlerRegistry[name] = handler;
        };

        yl.getForwardHandler = function (name) {
            return yl.forwardHandlerRegistry[name];
        };

        function getForwardStrategy(element) {
            var checkForCheckboxes = function () {
                var all = true;
                $.each(element, function (ix, e) {
                    if ($(e).attr("type") !== "checkbox") {
                        all = false;
                    }
                });
                return all;
            };

            if (element.length === 1 &&
                element.attr("type") === "checkbox" &&
                element.attr("value") === undefined) {
                // Single checkbox without 'value' attribute
                // Boolean field
                return "exists";
            } else if (element.length === 1 &&
                element.attr("multiple") !== undefined) {
                // Multiple by HTML semantics. E. g. multiple select
                // Multiple choice field
                return "multiple";
            } else if (checkForCheckboxes()) {
                // Multiple checkboxes or one checkbox with 'value' attribute.
                // Multiple choice field represented by checkboxes
                return "multiple";
            } else {
                // Other cases
                return "single";
            }
        }

        /**
         * Get fields with name `name` relative to `element` with considering form
         * prefixes.
         * @param element the element
         * @param name name of the field
         * @returns jQuery object with found fields or empty jQuery object if no
         * field was found
         */
        yl.getFieldRelativeTo = function (element, name) {
            var prefixes = $(element).getFormPrefixes();

            for (var i = 0; i < prefixes.length; i++) {
                var fieldSelector = "[name=" + prefixes[i] + name + "]";
                var field = $(fieldSelector);

                if (field.length) {
                    return field;
                }
            }

            return $();
        };

        /**
         * Get field value which is put to forwarded dictionary
         * @param field the field
         * @returns forwarded value
         */
        yl.getValueFromField = function (field) {
            var strategy = getForwardStrategy(field);
            var serializedField = $(field).serializeArray();

            if ((serializedField == false) && ($(field).prop('disabled'))) {
                $(field).prop('disabled', false);
                serializedField = $(field).serializeArray();
                $(field).prop('disabled', true);
            }

            var getSerializedFieldElementAt = function (index) {
                // Return serializedField[index]
                // or null if something went wrong
                if (serializedField.length > index) {
                    return serializedField[index];
                } else {
                    return null;
                }
            };

            var getValueOf = function (elem) {
                // Return elem.value
                // or null if something went wrong
                if (elem.hasOwnProperty("value") &&
                    elem.value !== undefined
                ) {
                    return elem.value;
                } else {
                    return null;
                }
            };

            var getSerializedFieldValueAt = function (index) {
                // Return serializedField[index].value
                // or null if something went wrong
                var elem = getSerializedFieldElementAt(index);
                if (elem !== null) {
                    return getValueOf(elem);
                } else {
                    return null;
                }
            };

            if (strategy === "multiple") {
                return serializedField.map(
                    function (item) {
                        return getValueOf(item);
                    }
                );
            } else if (strategy === "exists") {
                return serializedField.length > 0;
            } else {
                return getSerializedFieldValueAt(0);
            }
        };

        yl.getForwards = function (element) {
            var forwardElem,
                forwardList,
                forwardedData,
                divSelector,
                form;
            divSelector = "div.dal-forward-conf#dal-forward-conf-for-" +
                element.attr("id") + ", " +
                "div.dal-forward-conf#dal-forward-conf-for_" +
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

            forwardedData = {};

            $.each(forwardList, function (ix, field) {
                var srcName, dstName;
                if (field.type === "const") {
                    forwardedData[field.dst] = field.val;
                } else if (field.type === "self") {
                    if (field.hasOwnProperty("dst")) {
                        dstName = field.dst;
                    } else {
                        dstName = "self";
                    }
                    forwardedData[dstName] = yl.getValueFromField(element);
                } else if (field.type === "field") {
                    srcName = field.src;
                    if (field.hasOwnProperty("dst")) {
                        dstName = field.dst;
                    } else {
                        dstName = srcName;
                    }
                    var forwardedField = yl.getFieldRelativeTo(element, srcName);

                    if (!forwardedField.length) {
                        return;
                    }

                    forwardedData[dstName] = yl.getValueFromField(forwardedField);
                } else if (field.type === "javascript") {
                    var handler = yl.getForwardHandler(field.handler);
                    forwardedData[field.dst || field.handler] = handler(element);
                }

            });
            return JSON.stringify(forwardedData);
        };

    })(django.jQuery, yl);

    (function ($) {
        if (window.__dal__initListenerIsSet)
            return;

        $(document).on('autocompleteLightInitialize', '[data-autocomplete-light-function=select2]', function () {
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
                var text = template(item.text,
                    element.attr('data-html') !== undefined || element.attr('data-result-html') !== undefined
                );

                if (item.create_id) {
                    return $('<span></span>').text(text).addClass('dal-create')
                } else {
                    return text
                }
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
                            forward: yl.getForwards(element)
                        };

                        return data;
                    },
                    processResults: function (data, page) {
                        if (element.attr('data-tags')) {
                            $.each(data.results, function (index, value) {
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
                containerCssClass: ':all:',
                placeholder: element.attr('data-placeholder') || '',
                language: element.attr('data-autocomplete-light-language'),
                minimumInputLength: element.attr('data-minimum-input-length') || 0,
                allowClear: !$(this).is('[required]'),
                templateResult: result_template,
                templateSelection: selected_template,
                ajax: ajax,
                with: null,
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
                        forward: yl.getForwards($(this))
                    },
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", document.csrftoken);
                    },
                    success: function (data, textStatus, jqXHR) {
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
        $('[data-autocomplete-light-function=select2]:not([id*="__prefix__"])').each(function () {
            window.__dal__initialize(this);
        });
    })(django.jQuery);
});