import $ from "jquery";

/**
 * Converts a grp.jQuery instance to a django.jQuery instance.
 */
function django$($sel) {
  if (typeof window.grp === "undefined") {
    return $($sel);
  }
  if (window.grp.jQuery.fn.init === $.fn.init) {
    return $($sel);
  }
  const $djangoSel = $($sel);
  if ($sel.prevObject) {
    $djangoSel.prevObject = django$($sel.prevObject);
  }
  return $djangoSel;
}

export default django$;
