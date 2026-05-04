import $ from "jquery";

var prefixCache = {};

$.fn.djnData = function (name) {
  var inlineFormsetData = $(this).data("inlineFormset") || {},
    nestedOptions = inlineFormsetData.nestedOptions || {};
  if (!name) {
    return nestedOptions;
  } else {
    return nestedOptions[name];
  }
};

$.fn.djangoPrefixIndex = function () {
  var $this = this.length > 1 ? this.first() : this;
  var id = $this.attr("id"),
    name = $this.attr("name"),
    forattr = $this.attr("for"),
    prefix,
    $form,
    $group,
    groupId,
    cacheKey,
    match,
    index;

  if (
    (match = prefixCache[id]) ||
    (match = prefixCache[name]) ||
    (match = prefixCache[forattr])
  ) {
    return match;
  }

  if (id && !prefix) {
    prefix = (id.match(/^(.*)\-group$/) || [null, null])[1];
  }

  if (id && !prefix && $this.is(".djn-item") && id.match(/\d+$/)) {
    [cacheKey, prefix, index] = id.match(/(.*?)\-(\d+)$/) || [null, null, null];
  }

  if (!prefix) {
    $form = $this.closest(".djn-inline-form");
    if ($form.length) {
      [cacheKey, prefix, index] = $form.attr("id").match(/(.*?)\-(\d+)$/) || [
        null,
        null,
        null,
      ];
    } else {
      $group = $this.closest(".djn-group");
      if (!$group.length) {
        return null;
      }
      groupId = $group.attr("id") || "";
      prefix = (groupId.match(/^(.*)\-group$/) || [null, null])[1];
    }
  } else {
    if (prefix.substr(0, 3) == "id_") {
      prefix = prefix.substr(3);
    }

    if (!document.getElementById(prefix + "-group")) {
      return null;
    }
  }
  if (cacheKey) {
    prefixCache[cacheKey] = [prefix, index];
  }

  return [prefix, index];
};

$.fn.djangoFormPrefix = function () {
  var prefixIndex = this.djangoPrefixIndex();
  if (!prefixIndex || !prefixIndex[1]) {
    return null;
  }
  return prefixIndex[0] + "-" + prefixIndex[1] + "-";
};

$.fn.djangoFormIndex = function () {
  var prefixIndex = this.djangoPrefixIndex();
  return !prefixIndex || !prefixIndex[1] ? null : parseInt(prefixIndex[1], 10);
};

$.fn.djangoFormsetPrefix = function () {
  var prefixIndex = this.djangoPrefixIndex();
  return !prefixIndex ? null : prefixIndex[0];
};

var filterDjangoFormsetForms = function (form, $group, formsetPrefix) {
  var formId = form.getAttribute("id"),
    formIndex = formId.substr(formsetPrefix.length + 1);

  // Check if form id matches /{prefix}-\d+/
  if (formId.indexOf(formsetPrefix) !== 0) {
    return false;
  }
  return !formIndex.match(/\D/);
};

// Selects all initial forms within the same formset as the
// element the method is being called on.
$.fn.djangoFormsetForms = function () {
  var forms = [];
  this.each(function () {
    var $this = $(this),
      formsetPrefix = $this.djangoFormsetPrefix(),
      $group = formsetPrefix ? $("#" + formsetPrefix + "-group") : null,
      $forms;

    if (!formsetPrefix || !$group.length) return;

    $forms = $group.find(".djn-inline-form").filter(function () {
      return filterDjangoFormsetForms(this, $group, formsetPrefix);
    });
    var sortedForms = $forms.toArray().sort(function (a, b) {
      return $(a).djangoFormIndex() - $(b).djangoFormIndex;
    });
    Array.prototype.push.apply(forms, sortedForms);
  });
  return this.pushStack(forms);
};

if (typeof $.djangoFormField != "function") {
  $.djangoFormField = function (fieldName, prefix, index) {
    var $empty = $([]),
      matches;
    if ((matches = prefix.match(/^(.+)\-(\d+)\-$/))) {
      prefix = matches[1];
      index = matches[2];
    }
    index = parseInt(index, 10);
    if (isNaN(index)) {
      return $empty;
    }
    var namePrefix = prefix + "-" + index + "-";
    if (fieldName == "*") {
      return $('*[name^="' + namePrefix + '"]').filter(function () {
        var fieldPart = $(this).attr("name").substring(namePrefix.length);
        return fieldPart.indexOf("-") === -1;
      });
    }
    var $field = $("#id_" + namePrefix + fieldName);
    if (!$field.length && (fieldName == "pk" || fieldName == "position")) {
      var $group = $("#" + prefix + "-group"),
        fieldNameData = $group.djnData("fieldNames") || {};
      fieldName = fieldNameData[fieldName];
      if (!fieldName) {
        return $empty;
      }
      $field = $("#id_" + namePrefix + fieldName);
    }
    return $field;
  };
}

if (typeof $.fn.djangoFormField != "function") {
  /**
   * Given a django model's field name, and the forms index in the
   * formset, returns the field's input element, or an empty jQuery
   * object on failure.
   *
   * @param String fieldName - 'pk', 'position', or the field's
   *                           name in django (e.g. 'content_type',
   *                           'url', etc.)
   * @return jQuery object containing the field's input element, or
   *         an empty jQuery object on failure
   */
  $.fn.djangoFormField = function (fieldName, index) {
    var prefixAndIndex = this.djangoPrefixIndex();
    var $empty = $([]);
    if (!prefixAndIndex) {
      return $empty;
    }
    var prefix = prefixAndIndex[0];
    if (typeof index == "undefined") {
      index = prefixAndIndex[1];
      if (typeof index == "undefined") {
        return $empty;
      }
    }
    return $.djangoFormField(fieldName, prefix, index);
  };
}

if (typeof $.fn.filterDjangoField != "function") {
  var djRegexCache = {};
  $.fn.filterDjangoField = function (prefix, fieldName, index) {
    var $field, fieldNameData;
    if (typeof index != "undefined") {
      if (typeof index == "string") {
        index = parseInt(index, 10);
      }
      if (typeof index == "number" && !isNaN(index)) {
        var fieldId = "id_" + prefix + "-" + index + "-" + fieldName;
        $field = $("#" + fieldId);
      }
    } else {
      if (typeof djRegexCache[prefix] != "object") {
        djRegexCache[prefix] = {};
      }
      if (typeof djRegexCache[prefix][fieldName] == "undefined") {
        djRegexCache[prefix][fieldName] = new RegExp(
          "^" + prefix + "-\\d+-" + fieldName + "$"
        );
      }
      $field = this.find('input[name$="' + fieldName + '"]').filter(
        function () {
          return this.getAttribute("name").match(
            djRegexCache[prefix][fieldName]
          );
        }
      );
    }
    if (!$field.length && (fieldName == "pk" || fieldName == "position")) {
      fieldNameData = $("#" + prefix + "-group").djnData("fieldNames") || {};
      if (
        typeof fieldNameData[fieldName] &&
        fieldNameData[fieldName] != fieldName
      ) {
        $field = $(this).filterDjangoField(
          prefix,
          fieldNameData[fieldName],
          index
        );
      }
    }
    return $field;
  };
}
