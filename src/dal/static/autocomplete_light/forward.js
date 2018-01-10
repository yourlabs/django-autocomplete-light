;(function($, yl) {
    yl.forwardHandlerRegistry = yl.forwardHandlerRegistry || {};

    yl.registerForwardHandler = function(name, handler) {
        yl.forwardHandlerRegistry[name] = handler;
    };

    yl.getForwardHandler = function(name) {
        return yl.forwardHandlerRegistry[name];
    };

    function getForwardStrategy(element) {
        var checkForCheckboxes = function() {
            var all = true;
            $.each(element, function(ix, e) {
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
    yl.getFieldRelativeTo = function(element, name) {
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
    yl.getValueFromField = function(field) {
        var strategy = getForwardStrategy(field);
        var serializedField = $(field).serializeArray();

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

    yl.getForwards = function(element) {
        var forwardElem,
            forwardList,
            forwardedData,
            divSelector,
            form;
        divSelector = "div.dal-forward-conf#dal-forward-conf-for-" +
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

        $.each(forwardList, function(ix, field) {
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

})(yl.jQuery, yl);
