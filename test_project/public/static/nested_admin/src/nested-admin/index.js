import $ from "jquery";
import * as grappelli from "grappelli";
import DJNesting from "./utils";
import DjangoFormset from "./jquery.djangoformset";

DJNesting.DjangoFormset = DjangoFormset;

$(document).ready(function () {
  // Remove the border on any empty fieldsets
  $("fieldset.grp-module, fieldset.module")
    .filter(function (i, element) {
      return element.childNodes.length == 0;
    })
    .css("border-width", "0");

  // Set predelete class on any form elements with the DELETE input checked.
  // These can occur on forms rendered after a validation error.
  $('input[name$="-DELETE"]:checked')
    .not('[name*="__prefix__"]')
    .closest(".djn-inline-form")
    .addClass("grp-predelete");

  $(document).on(
    "djnesting:initialized djnesting:mutate",
    function onMutate(e, $inline) {
      var $items = $inline.find(
        "> .djn-items, > .tabular > .module > .djn-items"
      );
      var $rows = $items.children(".djn-tbody");
      $rows.removeClass("row1 row2");
      $rows.each(function (i, row) {
        var n = 1 + (i % 2);
        $(row).addClass("row" + n);
      });
    }
  );

  // Register the nested formset on top level djnesting-stacked elements.
  // It will handle recursing down the nested inlines.
  $(".djn-group-root").each(function (i, rootGroup) {
    $(rootGroup).djangoFormset();
  });

  $("form").on("submit.djnesting", function (e) {
    $(".djn-group").each(function () {
      DJNesting.updatePositions($(this).djangoFormsetPrefix());
      $(document).trigger("djnesting:mutate", [
        $(this).djangoFormset().$inline,
      ]);
    });
  });
});

export default DJNesting;
