import $ from "jquery";

/**
 * For grappelli 2.14, converts a django.jQuery instance to a grp.jQuery
 * instance. Otherwise (if grappelli is not present, or for grappelli <= 2.13,
 * where the grappelli jQuery instance is the same as django's), returns the
 * object that was passed in, unchanged.
 */
function grp$($sel) {
  if (typeof window.grp === "undefined") {
    return $($sel);
  }
  if (window.grp.jQuery.fn.init === $.fn.init) {
    return $($sel);
  }
  const $grpSel = window.grp.jQuery($sel);
  if ($sel.prevObject) {
    $grpSel.prevObject = grp$($sel.prevObject);
  }
  return $grpSel;
}

export default grp$;
