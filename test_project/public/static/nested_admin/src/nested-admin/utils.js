/* globals SelectFilter, DateTimeShortcuts */
import $ from "jquery";
import "./jquery.djnutils";
import { createSortable, updatePositions } from "./sortable";
import regexQuote from "./regexquote";
import django$ from "./django$";
import grp$ from "./grp$";

var DJNesting = typeof window.DJNesting != "undefined" ? window.DJNesting : {};

DJNesting.regexQuote = regexQuote;
DJNesting.createSortable = createSortable;
DJNesting.updatePositions = updatePositions;

/**
 * Update attributes based on a regular expression
 */
DJNesting.updateFormAttributes = function ($elem, search, replace, selector) {
  if (!selector) {
    selector = [
      ":input",
      "span",
      "table",
      "iframe",
      "label",
      "a",
      "ul",
      "p",
      "img",
      ".djn-group",
      ".djn-inline-form",
      ".cropduster-form",
      ".dal-forward-conf",
    ].join(",");
  }
  var addBackMethod = $.fn.addBack ? "addBack" : "andSelf";
  $elem
    .find(selector)
    [addBackMethod]()
    .each(function () {
      var $node = $(this),
        attrs = [
          "id",
          "name",
          "for",
          "href",
          "class",
          "onclick",
          "data-inline-formset",
        ];

      $.each(attrs, function (i, attrName) {
        var attrVal = $node.attr(attrName);
        if (attrVal) {
          $node.attr(attrName, attrVal.replace(search, replace));
          if (attrName === "data-inline-formset") {
            $node.data("inlineFormset", JSON.parse($node.attr(attrName)));
          }
        }
      });
    });
  // update prepopulate ids for function initPrepopulatedFields
  $elem.find(".prepopulated_field").each(function () {
    var $node = grp$(this);
    if (typeof $node.prepopulate !== "function") {
      $node = django$(this);
    }
    var dependencyIds = $.makeArray($node.data("dependency_ids") || []);
    $node.data(
      "dependency_ids",
      $.map(dependencyIds, function (id) {
        return id.replace(search, replace);
      })
    );
  });
};

DJNesting.createContainerElement = function () {
  return;
};

// Slight tweaks to the grappelli functions of the same name
// (initRelatedFields and initAutocompleteFields).
//
// The most notable tweak is the call to $.fn.grp_related_generic() (a
// jQuery method provided by django-curated) and the use of
// DJNesting.LOOKUP_URLS to determine the ajax lookup urls.
//
// We abstract this out using form prefix because the way grappelli does it
// (adding javascript at the bottom of each formset) doesn't really scale
// with nested formsets.

// The second parameter (groupData) is optional, and only exists to prevent
// redundant calls to jQuery() and jQuery.fn.data() in the calling context
DJNesting.initRelatedFields = function (prefix, groupData) {
  if (
    typeof DJNesting.LOOKUP_URLS != "object" ||
    !DJNesting.LOOKUP_URLS.related
  ) {
    return;
  }
  var lookupUrls = DJNesting.LOOKUP_URLS;
  var $inline = $("#" + prefix + "-group");

  if (!groupData) {
    groupData = $inline.djnData();
  }
  var lookupFields = groupData.lookupRelated;

  $inline.djangoFormsetForms().each(function (i, form) {
    $.each(lookupFields.fk || [], function (i, fk) {
      $(form)
        .djangoFormField(fk)
        .each(function () {
          grp$(this).grp_related_fk({
            lookup_url: lookupUrls.related,
          });
        });
    });
    $.each(lookupFields.m2m || [], function (i, m2m) {
      $(form)
        .djangoFormField(m2m)
        .each(function () {
          grp$(this).grp_related_m2m({ lookup_url: lookupUrls.m2m });
        });
    });
    $.each(lookupFields.generic || [], function () {
      var [contentType, objectId] = this;
      $(form)
        .djangoFormField(objectId)
        .each(function () {
          var $this = $(this);
          var index = $this.djangoFormIndex();
          if ($this.hasClass("grp-has-related-lookup")) {
            $this.parent().find("a.related-lookup").remove();
            $this.parent().find(".grp-placeholder-related-generic").remove();
          }
          grp$($this).grp_related_generic({
            content_type: `#id_${prefix}-${index}-${contentType}`,
            object_id: `#id_${prefix}-${index}-${objectId}`,
            lookup_url: lookupUrls.related,
          });
        });
    });
  });
};

DJNesting.initAutocompleteFields = function (prefix, groupData) {
  if (
    typeof DJNesting.LOOKUP_URLS != "object" ||
    !DJNesting.LOOKUP_URLS.related
  ) {
    return;
  }
  var lookupUrls = DJNesting.LOOKUP_URLS;

  var $inline = $("#" + prefix + "-group");

  if (!groupData) {
    groupData = $inline.djnData();
  }
  var lookupFields = groupData.lookupAutocomplete;

  $inline.djangoFormsetForms().each(function (i, form) {
    $.each(lookupFields.fk || [], function (i, fk) {
      $(form)
        .djangoFormField(fk)
        .each(function () {
          var $this = $(this),
            id = $this.attr("id");
          // An autocomplete widget has already been initialized, return
          if ($("#" + id + "-autocomplete").length) {
            return;
          }
          grp$($this).grp_autocomplete_fk({
            lookup_url: lookupUrls.related,
            autocomplete_lookup_url: lookupUrls.autocomplete,
          });
        });
    });
    $.each(lookupFields.m2m || [], function (i, m2m) {
      $(form)
        .djangoFormField(m2m)
        .each(function () {
          var $this = $(this),
            id = $this.attr("id");
          // An autocomplete widget has already been initialized, return
          if ($("#" + id + "-autocomplete").length) {
            return;
          }
          grp$($this).grp_autocomplete_m2m({
            lookup_url: lookupUrls.m2m,
            autocomplete_lookup_url: lookupUrls.autocomplete,
          });
        });
    });
    $.each(lookupFields.generic || [], function () {
      var [contentType, objectId] = this;
      $(form)
        .djangoFormField(objectId)
        .each(function () {
          var $this = $(this);
          var index = $this.djangoFormIndex();
          // An autocomplete widget has already been initialized, return
          if ($("#" + $this.attr("id") + "-autocomplete").length) {
            return;
          }
          grp$($this).grp_autocomplete_generic({
            content_type: `#id_${prefix}-${index}-${contentType}`,
            object_id: `#id_${prefix}-${index}-${objectId}`,
            lookup_url: lookupUrls.related,
            autocomplete_lookup_url: lookupUrls.m2m,
          });
        });
    });
  });
};

function getLevelPrefix(id) {
  return id
    .replace(/^\#?id_/, "")
    .split(/-(?:empty|__prefix__|\d+)-/g)
    .slice(0, -1)
    .join("-");
}

// I very much regret that these are basically copy-pasted from django's
// inlines.js, but they're hidden in closure scope so I don't have much choice.
DJNesting.DjangoInlines = {
  initPrepopulatedFields: function (row) {
    const formPrefix = row.djangoFormPrefix();
    if (!formPrefix) return;
    const fields = $("#django-admin-prepopulated-fields-constants").data(
      "prepopulatedFields"
    );
    const fieldNames = new Set();
    const fieldDependencies = {};

    if (Array.isArray(fields)) {
      fields.forEach(
        ({ id, name, dependency_list, maxLength, allowUnicode }) => {
          fieldNames.add(name);
          const levelPrefix = getLevelPrefix(id);
          if (typeof fieldDependencies[levelPrefix] !== "object") {
            fieldDependencies[levelPrefix] = {};
          }
          fieldDependencies[levelPrefix][name] = {
            dependency_list,
            maxLength,
            allowUnicode,
          };
        }
      );
      fieldNames.forEach((name) => {
        row
          .find(`.form-row .field-${name}, .form-row.field-${name}`)
          .each(function () {
            const $el = $(this);
            const prefix = $el.djangoFormPrefix();
            if (!prefix) return;
            const levelPrefix = getLevelPrefix(prefix);
            const dep = (fieldDependencies[levelPrefix] || {})[name];
            if (dep) {
              $el.addClass("prepopulated_field");
              const $field = $el.is(":input") ? $el : $el.find(":input");
              $field.data("dependency_list", dep.dependency_list);
              $field.data("maxLength", dep.maxLength);
              $field.data("allowUnicode", dep.allowUnicode);
            }
          });
      });
    }
    if (formPrefix.match(/__prefix__/)) return;
    row.find(".prepopulated_field").each(function () {
      var field = $(this),
        input = field.is(":input") ? field : field.find(":input"),
        $input = grp$(input),
        inputFormPrefix = input.djangoFormPrefix(),
        dependencyList = $input.data("dependency_list") || [],
        dependencies = [];
      if (!inputFormPrefix || inputFormPrefix.match(/__prefix__/)) return;
      if (!dependencyList.length || !$input.prepopulate) {
        $input = django$(input);
        dependencyList = $input.data("dependency_list") || [];
      }
      $.each(dependencyList, function (i, fieldName) {
        dependencies.push("#id_" + inputFormPrefix + fieldName);
      });
      if (dependencies.length) {
        $input.prepopulate(
          dependencies,
          $input.data("maxLength") || $input.attr("maxlength"),
          $input.data("allowUnicode")
        );
      }
    });
  },
  reinitDateTimeShortCuts: function () {
    // Reinitialize the calendar and clock widgets by force
    if (typeof window.DateTimeShortcuts !== "undefined") {
      $(".datetimeshortcuts").remove();
      DateTimeShortcuts.init();
    }
  },
  updateSelectFilter: function ($form) {
    // If any SelectFilter widgets are a part of the new form,
    // instantiate a new SelectFilter instance for it.
    if (typeof window.SelectFilter !== "undefined") {
      $form.find(".selectfilter").each(function (index, value) {
        var namearr = value.name.split("-");
        SelectFilter.init(
          value.id,
          this.dataset.fieldName ?? namearr[namearr.length - 1],
          false
        );
      });
      $form.find(".selectfilterstacked").each(function (index, value) {
        var namearr = value.name.split("-");
        SelectFilter.init(
          value.id,
          this.dataset.fieldName ?? namearr[namearr.length - 1],
          true
        );
      });
    }
  },
};

function patchSelectFilter() {
  window.SelectFilter.init = (function (oldFn) {
    return function init(field_id, field_name, is_stacked) {
      if (field_id.match(/\-empty\-/)) {
        return;
      } else {
        oldFn.apply(this, arguments);
      }
    };
  })(window.SelectFilter.init);
}

if (typeof window.SelectFilter !== "undefined") {
  patchSelectFilter();
} else {
  setTimeout(function () {
    if (typeof window.SelectFilter !== "undefined") {
      patchSelectFilter();
    }
  }, 12);
}

function patchSelectBox() {
  window.SelectBox.init = (function (oldFn) {
    return function init(field_id, field_name, is_stacked) {
      if (field_id.match(/\-empty\-/)) {
        return;
      } else {
        oldFn.apply(this, arguments);
      }
    };
  })(window.SelectBox.init);
  window.SelectBox.add_to_cache = (function (oldFn) {
    return function add_to_cache(id, option) {
      if (!id.match(/_(from|to)$/)) return;
      return oldFn.apply(this, arguments);
    };
  })(window.SelectBox.add_to_cache);
  window.SelectBox.redisplay = (function (oldFn) {
    return function redisplay(id) {
      if (!id.match(/_(from|to)$/)) return;
      return oldFn.apply(this, arguments);
    };
  })(window.SelectBox.redisplay);
}

if (typeof window.SelectBox !== "undefined") {
  patchSelectBox();
} else {
  setTimeout(function () {
    if (typeof window.SelectBox !== "undefined") {
      patchSelectBox();
    }
  }, 12);
}

const djangoFuncs = ["prepopulate", "djangoAdminSelect2"];

djangoFuncs.forEach((funcName) => {
  (function patchDjangoFunction(callCount) {
    if (callCount > 2) {
      return;
    }
    if (typeof $.fn[funcName] === "undefined") {
      return setTimeout(() => patchDjangoFunction(++callCount), 12);
    }
    $.fn[funcName] = (function (oldFn) {
      return function django_fn_patch() {
        return oldFn.apply(
          this.filter(
            ':not([id*="-empty-"]):not([id$="-empty"]):not([id*="__prefix__"])'
          ),
          arguments
        );
      };
    })($.fn[funcName]);
  })(0);
});

const grpFuncs = [
  "grp_autocomplete_fk",
  "grp_autocomplete_generic",
  "grp_autocomplete_m2m",
  "grp_collapsible",
  "grp_collapsible_group",
  "grp_inline",
  "grp_related_fk",
  "grp_related_generic",
  "grp_related_m2m",
  "grp_timepicker",
  "datepicker",
  "prepopulate",
  "djangoAdminSelect2",
];

grpFuncs.forEach((funcName) => {
  (function patchGrpFunction(callCount) {
    if (callCount > 2) {
      return;
    }
    if (
      typeof window.grp === "undefined" ||
      typeof window.grp.jQuery.fn[funcName] === "undefined"
    ) {
      return setTimeout(() => patchGrpFunction(++callCount), 12);
    }
    window.grp.jQuery.fn[funcName] = (function (oldFn) {
      return function grp_fn_patch() {
        return oldFn.apply(
          this.filter(
            ':not([id*="-empty-"]):not([id$="-empty"]):not([id*="__prefix__"])'
          ),
          arguments
        );
      };
    })(window.grp.jQuery.fn[funcName]);
  })(0);
});

export default DJNesting;
