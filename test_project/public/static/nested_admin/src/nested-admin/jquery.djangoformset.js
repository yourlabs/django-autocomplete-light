import $ from "jquery";

import regexQuote from "./regexquote";
import DJNesting from "./utils";
import * as grappelli from "grappelli";
import grp from "grp";
import grp$ from "./grp$";
import django$ from "./django$";

var pluginName = "djangoFormset";

class DjangoFormset {
  constructor(inline) {
    this.opts = {
      emptyClass: "empty-form grp-empty-form djn-empty-form",
      predeleteClass: "grp-predelete",
    };
    this.$inline = $(inline);
    this.prefix = this.$inline.djangoFormsetPrefix();
    this._$totalForms = this.$inline.find(
      "#id_" + this.prefix + "-TOTAL_FORMS"
    );
    this._$totalForms.attr("autocomplete", "off");
    this._$template = $("#" + this.prefix + "-empty");

    var inlineModelClassName = this.$inline.djnData("inlineModel");
    const nestingLevel = this.$inline.djnData("nestingLevel");
    const handlerSelector = `.djn-model-${inlineModelClassName}.djn-level-${nestingLevel}`;

    this.opts = $.extend({}, this.opts, {
      childTypes: this.$inline.data("inlineFormset").options.childTypes,
      formsetFkModel: this.$inline.djnData("formsetFkModel"),
      addButtonSelector: ".djn-add-handler" + handlerSelector,
      removeButtonSelector: ".djn-remove-handler" + handlerSelector,
      deleteButtonSelector: ".djn-delete-handler" + handlerSelector,
      formClass:
        "dynamic-form grp-dynamic-form djn-dynamic-form-" +
        inlineModelClassName,
      formClassSelector: ".djn-dynamic-form-" + inlineModelClassName,
    });

    DJNesting.initRelatedFields(this.prefix, this.$inline.djnData());
    DJNesting.initAutocompleteFields(this.prefix, this.$inline.djnData());

    if (this.opts.childTypes) {
      this._setupPolymorphic();
    }
    this._bindEvents();

    this._initializeForms();

    this.$inline
      .find('.djn-items:not([id*="-empty"])')
      .trigger("djnesting:init");

    // initialize nested formsets
    this.$inline
      .find(
        '.djn-group[id$="-group"][id^="' +
          this.prefix +
          '"][data-inline-formset]:not([id*="-empty"])'
      )
      .each(function () {
        $(this)[pluginName]();
      });

    if (this.$inline.is(".djn-group-root")) {
      DJNesting.createSortable(this.$inline);
    }

    $(document).trigger("djnesting:initialized", [this.$inline, this]);
  }
  _setupPolymorphic() {
    if (!this.opts.childTypes) {
      throw Error(
        "The polymorphic fieldset options.childTypes is not defined!"
      );
    }
    let menu = '<div class="polymorphic-type-menu" style="display: none"><ul>';
    this.opts.childTypes.forEach((c) => {
      menu += `<li><a href="#" data-type="${c.type}">${c.name}</a></li>`;
    });
    menu += "</ul></div>";
    const $addButton = this.$inline.find(this.opts.addButtonSelector);
    const $menu = $(menu);
    $addButton.after($menu);
  }

  _initializeForms() {
    var totalForms = this.mgmtVal("TOTAL_FORMS");
    var maxForms = this.mgmtVal("MAX_NUM_FORMS");
    if (maxForms <= totalForms) {
      this.$inline
        .find(this.opts.addButtonSelector)
        .parents(".djn-add-item")
        .hide();
    }
    for (var i = 0; i < totalForms; i++) {
      this._initializeForm("#" + this.prefix + "-" + i);
    }
  }
  _initializeForm(form) {
    var $form = $(form);
    var formPrefix = $form.djangoFormPrefix();
    $form.addClass(this.opts.formClass);
    if ($form.hasClass("has_original")) {
      $("#id_" + formPrefix + "DELETE:checked").toggleClass(
        this.opts.predeleteClass
      );
    }
    var minForms = this.mgmtVal("MIN_NUM_FORMS");
    var totalForms = this.mgmtVal("TOTAL_FORMS");
    var self = this;
    var hideRemoveButton = totalForms <= minForms;
    this.$inline.djangoFormsetForms().each(function () {
      var showHideMethod = hideRemoveButton ? "hide" : "show";
      $(this).find(self.opts.removeButtonSelector)[showHideMethod]();
    });
  }
  _bindEvents($el) {
    var self = this;
    if (typeof $el == "undefined") {
      $el = this.$inline;
    }
    const $addButton = $el.find(this.opts.addButtonSelector);
    $addButton.off("click.djnesting").on("click.djnesting", function (e) {
      e.preventDefault();
      e.stopPropagation();
      const $menu = $(this).next(".polymorphic-type-menu");
      if (!$menu.length) {
        self.add();
      } else {
        if (!$menu.is(":visible")) {
          function hideMenu() {
            $menu.hide();
            $(document).off("click", hideMenu);
          }
          $(document).on("click", hideMenu);
        }
        $menu.show();
      }
    });
    const $menuButtons = $addButton.parent().find("> .polymorphic-type-menu a");
    $menuButtons.off("click.djnesting").on("click.djnesting", function (e) {
      e.preventDefault();
      e.stopPropagation();
      const polymorphicType = $(this).attr("data-type");
      self.add(null, polymorphicType);
      const $menu = $(e.target).closest(".polymorphic-type-menu");
      if ($menu.is(":visible")) {
        $menu.hide();
      }
    });
    $el
      .find(this.opts.removeButtonSelector)
      .filter(function () {
        return !$(this).closest(".djn-empty-form").length;
      })
      .off("click.djnesting")
      .on("click.djnesting", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var $form = $(this).closest(self.opts.formClassSelector);
        self.remove($form);
      });

    var deleteClickHandler = function (e) {
      e.preventDefault();
      e.stopImmediatePropagation();
      var $form = $(this).closest(self.opts.formClassSelector);
      var $deleteInput = $("#id_" + $form.djangoFormPrefix() + "DELETE");
      if (!$deleteInput.is(":checked")) {
        self["delete"]($form);
      } else {
        self.undelete($form);
      }
    };

    var $deleteButton = $el
      .find(this.opts.deleteButtonSelector)
      .filter(function () {
        return !$(this).closest(".djn-empty-form").length;
      });

    $deleteButton
      .off("click.djnesting")
      .on("click.djnesting", deleteClickHandler);
    $deleteButton
      .find('[id$="-DELETE"]')
      .on("mousedown.djnesting", deleteClickHandler);
  }
  remove(form) {
    var $form = $(form);
    var totalForms = this.mgmtVal("TOTAL_FORMS");
    var minForms = this.mgmtVal("MIN_NUM_FORMS");
    var maxForms = this.mgmtVal("MAX_NUM_FORMS");
    var index = $form.djangoFormIndex();
    var isInitial = $form.data("isInitial");

    // Clearing out the form HTML itself using DOM APIs is much faster
    // than using jQuery to remove the element. Using jQuery is so
    // slow that it hangs the page.
    $form[0].innerHTML = "";
    $form.remove();

    totalForms -= 1;
    this.mgmtVal("TOTAL_FORMS", totalForms);

    if (maxForms - totalForms >= 0) {
      this.$inline
        .find(this.opts.addButtonSelector)
        .parent(".djn-add-item,li")
        .show();
    }

    this._fillGap(index, isInitial);

    var self = this;
    var hideRemoveButton = totalForms <= minForms;
    this.$inline.djangoFormsetForms().each(function () {
      var showHideMethod = hideRemoveButton ? "hide" : "show";
      $(this).find(self.opts.removeButtonSelector)[showHideMethod]();
    });

    DJNesting.updatePositions(this.prefix);
    $(document).trigger("djnesting:mutate", [this.$inline]);

    // Also fire using the events that were added in Django 1.9
    $(document).trigger("formset:removed", [$form, this.prefix]);

    document.dispatchEvent(
      new CustomEvent("formset:removed", {
        detail: {
          formsetName: this.prefix,
        },
      })
    );
  }
  delete(form) {
    var self = this,
      $form = $(form),
      formPrefix = $form.djangoFormPrefix(),
      $deleteInput = $("#id_" + formPrefix + "DELETE");

    if ($form.hasClass(this.opts.predeleteClass)) {
      return;
    }

    if (!$form.data("isInitial")) {
      return;
    }
    $deleteInput.attr("checked", "checked");
    if ($deleteInput.length) {
      $deleteInput[0].checked = true;
    }
    $form.addClass(this.opts.predeleteClass);

    $form.find(".djn-group").each(function () {
      var $childInline = $(this);
      var childFormset = $childInline.djangoFormset();
      $childInline.djangoFormsetForms().each(function () {
        if ($(this).hasClass(self.opts.predeleteClass)) {
          $(this).data("alreadyDeleted", true);
        } else {
          childFormset.delete(this);
        }
      });
    });
    $form.find(".cropduster-form").each(function () {
      var formPrefix = $(this).djangoFormsetPrefix() + "-0-";
      var $deleteInput = $("#id_" + formPrefix + "DELETE");
      $deleteInput.attr("checked", "checked");
      if ($deleteInput.length) {
        $deleteInput[0].checked = true;
      }
    });
    DJNesting.updatePositions(this.prefix);
    $(document).trigger("djnesting:mutate", [this.$inline]);
    $(document).trigger("formset:deleted", [$form, this.prefix]);
  }
  undelete(form) {
    var $form = $(form),
      formPrefix = $form.djangoFormPrefix(),
      $deleteInput = $("#id_" + formPrefix + "DELETE");

    if ($form.parent().closest("." + this.opts.predeleteClass).length) {
      return;
    }
    if ($form.hasClass("has_original")) {
      $deleteInput.removeAttr("checked");
      if ($deleteInput.length) {
        $deleteInput[0].checked = false;
      }
      $form.removeClass(this.opts.predeleteClass);
    }
    $form.data("alreadyDeleted", false);
    $form.find(".djn-group").each(function () {
      var $childInline = $(this);
      var childFormset = $childInline.djangoFormset();
      $childInline.djangoFormsetForms().each(function () {
        if ($(this).data("alreadyDeleted")) {
          $(this).data("alreadyDeleted", false);
        } else {
          childFormset.undelete(this);
        }
      });
    });
    $form.find(".cropduster-form").each(function () {
      var formPrefix = $(this).djangoFormsetPrefix() + "-0-";
      var $deleteInput = $("#id_" + formPrefix + "DELETE");
      $deleteInput.removeAttr("checked");
      if ($deleteInput.length) {
        $deleteInput[0].checked = false;
      }
    });
    DJNesting.updatePositions(this.prefix);
    $(document).trigger("djnesting:mutate", [this.$inline]);
    $(document).trigger("formset:undeleted", [$form, this.prefix]);
  }
  add(spliceIndex, ctype) {
    var self = this;
    const $template = ctype
      ? $(`#${this.prefix}-empty-${ctype}`)
      : this._$template;
    var $form = $template.clone(true);

    // For django-grappelli >= 2.14, where the grp.jQuery instance is not
    // the same as django.jQuery, we must copy any prepopulated_field
    // dependency data from grp.jQuery to the cloned nodes.
    grp$($template)
      .find(":data(dependency_ids)")
      .each(function () {
        const id = $(this).attr("id");
        const $el = $form.find(`#${id}`);
        grp$($el).data($.extend({}, $el.data(), grp$(this).data()));
      });

    var index = this.mgmtVal("TOTAL_FORMS");
    var maxForms = this.mgmtVal("MAX_NUM_FORMS");
    var isNested = this.$inline.hasClass("djn-group-nested");

    $(document).trigger("djnesting:beforeadded", [this.$inline, $form]);

    $form.removeClass(this.opts.emptyClass);
    $form.addClass("djn-item");
    $form.attr("id", $form.attr("id").replace(/\-empty.*?$/, "-" + index));

    if (isNested) {
      $form.append(DJNesting.createContainerElement());
    }

    DJNesting.updateFormAttributes(
      $form,
      new RegExp(
        '([#_]id_|[\\#]|^id_|"|^)' +
          regexQuote(this.prefix) +
          "\\-(?:__prefix__|empty)\\-",
        "g"
      ),
      "$1" + this.prefix + "-" + index + "-"
    );

    let $firstTemplate = this._$template;
    if (this.opts.childTypes) {
      $firstTemplate = $template
        .closest(".djn-group")
        .find(
          '> .djn-items > [id*="-empty"], > .djn-fieldset > .djn-items > [id*="-empty"]'
        )
        .eq(0);
    }
    if (this.opts.childTypes) {
      const compatibleParents = this.$inline.djnData("compatibleParents") || {};
      $form.find("> .djn-group").each((i, el) => {
        const fkModel = $(el).djnData("formsetFkModel");
        const compatModels = compatibleParents[ctype] || [];
        const $el = $(el);
        const parentModel = $el.djnData("inlineParentModel");
        const isPolymorphic = !!$el.data("inlineFormset").options.childTypes;
        const formPrefix = $el.data("inlineFormset").options.prefix;
        if (
          parentModel !== ctype ||
          (isPolymorphic &&
            fkModel !== ctype &&
            compatModels.indexOf(fkModel) === -1)
        ) {
          $el.find('input[id$="_FORMS"]').each((i, input) => {
            input.value = 0;
            input.setAttribute("value", "0");
            el.parentNode.appendChild(input);
          });
          el.parentNode.removeChild(el);
        }
      });
    }

    $form.insertBefore($firstTemplate);

    this.mgmtVal("TOTAL_FORMS", index + 1);
    if (maxForms - (index + 1) <= 0) {
      this.$inline
        .find(this.opts.addButtonSelector)
        .parent(".djn-add-item,li")
        .hide();
    }

    DJNesting.updatePositions(this.prefix);

    if ($.isNumeric(spliceIndex)) {
      this.spliceInto($form, spliceIndex, true);
    } else {
      $(document).trigger("djnesting:mutate", [this.$inline]);
    }

    if (grappelli) {
      grappelli.reinitDateTimeFields(grp$($form));
    }
    DJNesting.DjangoInlines.initPrepopulatedFields(django$($form));
    DJNesting.DjangoInlines.reinitDateTimeShortCuts();
    DJNesting.DjangoInlines.updateSelectFilter($form);
    DJNesting.initRelatedFields(this.prefix);
    DJNesting.initAutocompleteFields(this.prefix);
    if (grp && grp.jQuery.fn.grp_collapsible) {
      var addBackMethod = grp.jQuery.fn.addBack ? "addBack" : "andSelf";
      grp$($form)
        .find('.grp-collapse:not([id$="-empty"]):not([id*="-empty-"])')
        [addBackMethod]()
        .grp_collapsible({
          toggle_handler_slctr: ".grp-collapse-handler:first",
          closed_css: "closed grp-closed",
          open_css: "open grp-open",
          on_toggle: function () {
            $(document).trigger("djnesting:toggle", [self.$inline]);
          },
        });
    }
    if (typeof $.fn.curated_content_type == "function") {
      $form.find(".curated-content-type-select").each(function () {
        $(this).curated_content_type();
      });
    }

    this._initializeForm($form);
    this._bindEvents($form);

    if (ctype) {
      const formsetModelClassName = this.$inline.djnData("inlineModel");
      const inlineModelClassName = $form.attr("data-inline-model");
      const $buttons = $form.find(`.djn-model-${formsetModelClassName}`);
      $buttons.addClass(`djn-model-${inlineModelClassName}`);
      $form.addClass(`djn-dynamic-form-${inlineModelClassName}`);
    }

    // find any nested formsets
    $form
      .find(
        '.djn-group[id$="-group"][id^="' +
          this.prefix +
          '"][data-inline-formset]:not([id*="-empty"])'
      )
      .each(function () {
        $(this)[pluginName]();
      });

    // Fire an event on the document so other javascript applications
    // can be alerted to the newly inserted inline
    $(document).trigger("djnesting:added", [this.$inline, $form]);

    // Also fire using the events that were added in Django 1.9
    $(document).trigger("formset:added", [$form, this.prefix]);

    try {
      $form.get(0).dispatchEvent(
        new CustomEvent("formset:added", {
          bubbles: true,
          detail: {
            formsetName: this.prefix,
          },
        })
      );
    } catch (e) {}

    return $form;
  }
  _fillGap(index, isInitial) {
    var $initialForm, $newForm;
    var formsets = this.$inline.djangoFormsetForms().toArray();
    // Sort formsets in index order, so that we get the last indexed form for the swap.
    formsets.sort(function (a, b) {
      return $(a).djangoFormIndex() - $(b).djangoFormIndex();
    });
    formsets.forEach(function (form) {
      var $form = $(form);
      var i = $form.djangoFormIndex();
      if (i <= index) {
        return;
      }
      if ($form.data("isInitial")) {
        $initialForm = $form;
      } else {
        $newForm = $form;
      }
    });
    var $form = isInitial ? $initialForm || $newForm : $newForm;
    if (!$form) {
      return;
    }
    var oldIndex = $form.djangoFormIndex();
    var oldFormPrefixRegex = new RegExp(
      "([\\#_]|^)" + regexQuote(this.prefix + "-" + oldIndex) + "(?!\\-\\d)"
    );
    $form.attr("id", this.prefix + "-" + index);
    DJNesting.updateFormAttributes(
      $form,
      oldFormPrefixRegex,
      "$1" + this.prefix + "-" + index
    );

    // Update prefixes on nested DjangoFormset objects
    $form.find(".djn-group").each(function () {
      var $childInline = $(this);
      var childFormset = $childInline.djangoFormset();
      childFormset.prefix = $childInline.djangoFormsetPrefix();
    });

    $(document).trigger("djnesting:attrchange", [this.$inline, $form]);

    if (isInitial && $initialForm && $newForm) {
      this._fillGap(oldIndex, false);
    }
  }
  _makeRoomForInsert() {
    var initialFormCount = this.mgmtVal("INITIAL_FORMS"),
      totalFormCount = this.mgmtVal("TOTAL_FORMS"),
      gapIndex = initialFormCount,
      $existingForm = $("#" + this.prefix + "-" + gapIndex);

    if (!$existingForm.length) {
      return;
    }

    var oldFormPrefixRegex = new RegExp(
      "([\\#_]|^)" + regexQuote(this.prefix) + "-" + gapIndex + "(?!\\-\\d)"
    );
    $existingForm.attr("id", this.prefix + "-" + totalFormCount);
    DJNesting.updateFormAttributes(
      $existingForm,
      oldFormPrefixRegex,
      "$1" + this.prefix + "-" + totalFormCount
    );

    // Update prefixes on nested DjangoFormset objects
    $existingForm.find(".djn-group").each(function () {
      var $childInline = $(this);
      var childFormset = $childInline.djangoFormset();
      childFormset.prefix = $childInline.djangoFormsetPrefix();
    });

    $(document).trigger("djnesting:attrchange", [this.$inline, $existingForm]);
  }
  /**
   * Splice a form into the current formset at new position `index`.
   */
  spliceInto($form, index, isNewAddition) {
    var initialFormCount = this.mgmtVal("INITIAL_FORMS"),
      totalFormCount = this.mgmtVal("TOTAL_FORMS"),
      oldFormsetPrefix = $form.djangoFormsetPrefix(),
      newFormsetPrefix = this.prefix,
      isInitial = $form.data("isInitial"),
      newIndex,
      $before;

    // Make sure the form being spliced is from a different inline
    if ($form.djangoFormsetPrefix() == this.prefix) {
      var currentPosition = $form.prevAll(
        ".djn-item:not(.djn-no-drag,.djn-thead)"
      ).length;
      if (currentPosition === index || typeof index == "undefined") {
        DJNesting.updatePositions(newFormsetPrefix);
        return;
      }
      $before = this.$inline
        .find("> .djn-items, > .tabular > .module > .djn-items")
        .find("> .djn-item:not(#" + $form.attr("id") + ")")
        .eq(index);
      $before.after($form);
    } else {
      var $oldInline = $("#" + oldFormsetPrefix + "-group");
      var $currentFormInline = $form.closest(".djn-group");

      if ($currentFormInline.djangoFormsetPrefix() != newFormsetPrefix) {
        $before = this.$inline
          .find("> .djn-items, > .tabular > .module > .djn-items")
          .find("> .djn-item")
          .eq(index);
        $before.after($form);
      }

      var oldDjangoFormset = $oldInline.djangoFormset();
      oldDjangoFormset.mgmtVal(
        "TOTAL_FORMS",
        oldDjangoFormset.mgmtVal("TOTAL_FORMS") - 1
      );
      oldDjangoFormset._fillGap($form.djangoFormIndex(), isInitial);

      if (isInitial) {
        oldDjangoFormset.mgmtVal(
          "INITIAL_FORMS",
          oldDjangoFormset.mgmtVal("INITIAL_FORMS") - 1
        );

        var $parentInline = this.$inline.parent().closest(".djn-group");
        if ($parentInline.length) {
          var $parentForm = this.$inline.closest(".djn-inline-form");
          var parentPkField = ($parentInline.djnData("fieldNames") || {}).pk;
          var $parentPk = $parentForm.djangoFormField(parentPkField);
          if (!$parentPk.val()) {
            $form.data("isInitial", false);
            $form.attr("data-is-initial", "false");
            isInitial = false;
            // Set initial form counts to 0 on nested DjangoFormsets
            setTimeout(function () {
              $form
                .find(
                  '[name^="' +
                    $form.djangoFormPrefix() +
                    '"][name$="-INITIAL_FORMS"]'
                )
                .val("0")
                .trigger("change");
            }, 0);
          }
        }
      }

      if (isInitial) {
        this._makeRoomForInsert();
      }

      // Replace the ids for the splice form
      var oldFormPrefixRegex = new RegExp(
        "([\\#_]|^)" + regexQuote($form.attr("id")) + "(?!\\-\\d)"
      );
      newIndex = isInitial ? initialFormCount : totalFormCount;
      $form.attr("id", newFormsetPrefix + "-" + newIndex);
      DJNesting.updateFormAttributes(
        $form,
        oldFormPrefixRegex,
        "$1" + newFormsetPrefix + "-" + newIndex
      );

      // Update prefixes on nested DjangoFormset objects
      $form.find(".djn-group").each(function () {
        var $childInline = $(this);
        var childFormset = $childInline.djangoFormset();
        childFormset.prefix = $childInline.djangoFormsetPrefix();
      });

      $(document).trigger("djnesting:attrchange", [this.$inline, $form]);

      if (isInitial) {
        this.mgmtVal("INITIAL_FORMS", initialFormCount + 1);
      }
      this.mgmtVal("TOTAL_FORMS", totalFormCount + 1);

      DJNesting.updatePositions(oldFormsetPrefix);
      $(document).trigger("djnesting:mutate", [$oldInline]);
    }

    DJNesting.updatePositions(newFormsetPrefix);
    if (!isNewAddition) {
      $(document).trigger("djnesting:mutate", [this.$inline]);
    }
  }
  mgmtVal(name, newValue) {
    var $field = this.$inline.find("#id_" + this.prefix + "-" + name);
    if (typeof newValue == "undefined") {
      return parseInt($field.val(), 10);
    } else {
      return parseInt($field.val(newValue).trigger("change").val(), 10);
    }
  }
}

$.fn[pluginName] = function () {
  var options, fn, args;
  var $el = this.eq(0);

  if (
    arguments.length === 0 ||
    (arguments.length === 1 && $.type(arguments[0]) != "string")
  ) {
    options = arguments[0];
    var djangoFormset = $el.data(pluginName);
    if (!djangoFormset) {
      djangoFormset = new DjangoFormset($el, options);
      $el.data(pluginName, djangoFormset);
    }
    return djangoFormset;
  }

  fn = arguments[0];
  args = $.makeArray(arguments).slice(1);

  if (fn in DjangoFormset.prototype) {
    return $el.data(pluginName)[fn](args);
  } else {
    throw new Error("Unknown function call " + fn + " for $.fn." + pluginName);
  }
};

export default DjangoFormset;
