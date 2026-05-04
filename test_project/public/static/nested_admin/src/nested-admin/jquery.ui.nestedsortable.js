import $ from "jquery";
import "./jquery.ui.djnsortable";

/*
 * jQuery UI Nested Sortable
 * v 1.3.4 / 28 apr 2011
 * http://mjsarfatti.com/sandbox/nestedSortable
 *
 * Depends:
 *    jquery.ui.sortable.js 1.8+
 *
 * License CC BY-SA 3.0
 * Copyright 2010-2011, Manuele J Sarfatti
 */
if (typeof $.fn.nearest != "function") {
  /**
   * Returns the descendant(s) matching a given selector which are the
   * shortest distance from the search context element (in otherwords,
   * $.fn.closest(), in reverse).
   */
  $.fn.nearest = function (selector) {
    var nearest = [],
      node = this,
      distance = 10000;
    node.find(selector).each(function () {
      var d = $(this).parentsUntil(node).length;
      if (d < distance) {
        distance = d;
        nearest = [this];
      } else if (d == distance) {
        nearest.push(this);
      }
    });
    return this.pushStack(nearest, "nearest", [selector]);
  };
}

var counter = 0;
var expando = "djn" + ("" + Math.random()).replace(/\D/g, "");

var createChildNestedSortable = function (parent, childContainer) {
  // Don't continue if the new element is the same as the old
  if (parent && parent.element && parent.element[0] == childContainer) {
    return;
  }
  var $childContainer = $(childContainer),
    options = $.extend({}, parent.options);
  options.connectWith = [parent.element];

  if ($childContainer.data(parent.widgetName)) {
    return;
  }

  var widgetConstructor = $childContainer[parent.widgetName];
  widgetConstructor.call($childContainer, options);
  var newInstance = $childContainer.data(parent.widgetName);
  for (var i = 0; i < parent.options.connectWith.length; i++) {
    var $otherContainer = parent.options.connectWith[i];
    newInstance.addToConnectWith($otherContainer);
    var otherInstance = $otherContainer.data(parent.widgetName);
    if (otherInstance) {
      otherInstance.addToConnectWith($childContainer);
    }
  }
  parent.addToConnectWith($childContainer);
  return newInstance;
};

$.widget("ui.nestedSortable", $.ui.djnsortable, {
  options: {
    tabSize: 20,
    disableNesting: "ui-nestedSortable-no-nesting",
    errorClass: "ui-nestedSortable-error",
    nestedContainerSelector: ":not(*)",
    // Whether to clear empty list item and container elements
    doNotClear: false,
    /**
     * Create a list container element if the draggable was dragged
     * to the top or bottom of the elements at its level.
     *
     * @param DOMElement parent - The element relative to which the
     *      new element will be inserted.
     * @return DOMElement - The new element.
     */
    createContainerElement: function (parent) {
      return $(document.createElement("ol"));
    },
    // Selector which matches all container elements in the nestedSortable
    containerElementSelector: "ol",
    // Selector which matches all list items (draggables) in the nestedSortable
    listItemSelector: "li",
    // Selector which, when applied to a container, returns its child list items
    items: "> li",
    maxLevels: 0,
    revertOnError: 1,
    protectRoot: false,
    rootID: null,
    rtl: false,
    // if true, you can not move nodes to different levels of nesting
    fixedNestingDepth: false,
    // show the error div or just not show a drop area
    showErrorDiv: true,
    // if true only allows you to rearrange within its parent container
    keepInParent: false,
    isAllowed: function (item, parent) {
      return true;
    },
    canConnectWith: function (container1, container2, instance) {
      var model1 = container1.data("inlineModel");
      var model2 = container2.data("inlineModel");
      if (model1 !== model2) {
        return false;
      }
      var instance2 = container2.data(instance.widgetName);
      if (!instance.options.fixedNestingDepth) {
        if (!instance2 || !instance2.options.fixedNestingDepth) {
          return true;
        }
      }
      var container1Level = instance._getLevel(container1);
      var container2Level = instance._getLevel(container2);
      return container1Level === container2Level;
    },
  },

  _createWidget: function (options, element) {
    var $element = $(element || this.defaultElement || this),
      dataOptions = $element.data("djnsortableOptions");
    element = $element[0];
    if (dataOptions) {
      options = $.extend({}, options, dataOptions);
    }
    return $.ui.djnsortable.prototype._createWidget.call(
      this,
      options,
      element
    );
  },

  _create: function () {
    if (this.element.data("uiNestedSortable")) {
      this.element.data(
        "nestedSortable",
        this.element.data("uiNestedSortable")
      );
    }
    if (this.element.data("ui-nestedSortable")) {
      this.element.data(
        "nestedSortable",
        this.element.data("ui-nestedSortable")
      );
    }
    this.element.data("djnsortable", this.element.data("nestedSortable"));
    if (this.element.data("uiNestedSortable")) {
      this.element.data("uiSortable", this.element.data("nestedSortable"));
    }
    // if (!this.element.is(this.options.containerElementSelector)) {
    //  throw new Error('nestedSortable: Please check that the ' +
    //                  'containerElementSelector option matches ' +
    //                  'the element passed to the constructor.');
    //             }

    $.ui.djnsortable.prototype._create.apply(this, arguments);

    this._connectWithMap = {};

    var self = this,
      o = this.options,
      $document = $(document);

    var originalConnectWith = o.connectWith;
    if (!originalConnectWith || typeof originalConnectWith == "string") {
      this.options.connectWith = [];
      if (typeof originalConnectWith == "string") {
        var connected = this._connectWith();
        for (var i = 0; i < connected.length; i++) {
          this.addToConnectWith($(connected[i]));
        }
      }

      // HACK!! FIX!! (django-specific logic)
      $document.on(
        "djnesting:init.nestedSortable",
        o.containerElementSelector,
        function (event) {
          createChildNestedSortable(self, this);
        }
      );
      this.element
        .find(o.containerElementSelector + ":not(.subarticle-wrapper)")
        .each(function (i, el) {
          if (
            $(el)
              .closest("[data-inline-formset]")
              .attr("id")
              .indexOf("-empty") > -1
          ) {
            return;
          }
          createChildNestedSortable(self, el);
        });
    }
    $document.trigger("nestedSortable:created", [this]);
    $document.on(
      "nestedSortable:created.nestedSortable",
      function (e, instance) {
        instance.addToConnectWith(self.element);
        self.addToConnectWith(instance.element);
      }
    );
  },

  addToConnectWith: function (element) {
    var self = this,
      $element = typeof element.selector != "undefined" ? element : $(element),
      uniqueId;

    if ($element.length > 1) {
      $element.each(function (i, el) {
        self.addToConnectWith($(el));
      });
      return;
    }
    uniqueId = element[0][expando];
    if (typeof uniqueId == "undefined") {
      uniqueId = element[0][expando] = ++counter;
    }
    if (typeof this.options.connectWith == "string") {
      return;
    }
    if (this._connectWithMap[uniqueId]) {
      return;
    }
    this.options.connectWith.push(element);
    this._connectWithMap[uniqueId] = 1;
  },

  _destroy: function () {
    this.element.removeData("nestedSortable").unbind(".nestedSortable");
    $(document).unbind(".nestedSortable");
    return $.ui.djnsortable.prototype.destroy.apply(this, arguments);
  },

  /**
   * Override this method to add extra conditions on an item before it's
   * rearranged.
   */
  _intersectsWithPointer: function _intersectsWithPointer(item) {
    var itemElement = item.item[0],
      o = this.options,
      intersection = $.ui.djnsortable.prototype._intersectsWithPointer.apply(
        this,
        arguments
      );

    this.lastItemElement = null;
    if (!intersection) {
      return intersection;
    }

    // Only put the placeholder inside the current Container, skip all
    // items from other containers. This works because when moving
    // an item from one container to another the
    // currentContainer is switched before the placeholder is moved.
    //
    // Without this moving items in "sub-sortables" can cause the placeholder to jitter
    // between the outer and inner container.
    if (item.instance !== this.currentContainer) {
      return false;
    }
    var $itemElement = $(itemElement);

    if (
      o.fixedNestingDepth &&
      this._getLevel(this.currentItem) === 1 + this._getLevel($itemElement)
    ) {
      $itemElement = (function () {
        var containerSel = o.containerElementSelector;
        var $childItems = $itemElement.find(".djn-item");
        if ($childItems.length != 1) {
          return $itemElement;
        }
        if (!$childItems.is(".djn-no-drag,.djn-thead")) {
          return $itemElement;
        }
        var itemElementClosestContainer = $itemElement.closest(containerSel);
        if (!itemElementClosestContainer.length) {
          return $itemElement;
        }
        // Make sure the item is only one level deeper
        if (
          itemElementClosestContainer[0] !=
          $childItems.closest(containerSel).closest(containerSel)[0]
        ) {
          return $itemElement;
        }
        return $($childItems[0]);
      })();
      itemElement = $itemElement[0];
    }

    if (
      itemElement != this.currentItem[0] && //cannot intersect with itself
      this.placeholder[intersection == 1 ? "next" : "prev"]()[0] !=
        itemElement && //no useless actions that have been done before
      !$.contains(this.placeholder[0], itemElement) && //no action if the item moved is the parent of the item checked
      (this.options.type == "semi-dynamic"
        ? !$.contains(this.element[0], itemElement)
        : true) &&
      (!o.keepInParent ||
        itemElement.parentNode == this.placeholder[0].parentNode) && //only rearrange items within the same container
      (!o.fixedNestingDepth ||
        this._getLevel(this.currentItem) === this._getLevel($itemElement)) && //maintain the nesting level of node
      (o.showErrorDiv ||
        o.isAllowed.call(
          this,
          this.currentItem[0],
          itemElement.parentNode,
          this.placeholder
        ))
    ) {
      this.lastItemElement = itemElement;
      return intersection;
    } else {
      return false;
    }
  },

  // This method is called after items have been iterated through.
  // Overriding this is cleaner than copying and pasting _mouseDrag()
  // and inserting logic in the middle.
  _contactContainers: function _contactContainers(event) {
    if (this.lastItemElement) {
      this._clearEmpty(this.lastItemElement);
    }

    var o = this.options,
      _parentItem = this.placeholder.closest(o.listItemSelector),
      parentItem =
        _parentItem.length && _parentItem.closest(".ui-sortable").length
          ? _parentItem
          : null,
      level = this._getLevel(this.placeholder),
      childLevels = this._getChildLevels(this.helper);

    var placeholderClassName = this.placeholder.attr("class");
    var phClassSearch = " " + placeholderClassName + " ";
    // If the current level class isn't already set
    if (
      phClassSearch.indexOf(" ui-sortable-nested-level-" + level + " ") == -1
    ) {
      var phOrigClassName;
      // Check if another level class is set
      var phOrigClassNameEndPos =
        phClassSearch.indexOf(" ui-sortable-nested-level-") - 1;
      if (phOrigClassNameEndPos > -1) {
        phOrigClassName = placeholderClassName.substring(
          0,
          phOrigClassNameEndPos
        );
      } else {
        phOrigClassName = placeholderClassName;
      }
      // Add new level to class
      this.placeholder.attr(
        "class",
        phOrigClassName + " ui-sortable-nested-level-" + level
      );
    }

    // To find the previous sibling in the list, keep backtracking until we hit a valid list item.
    var previousItem = this.placeholder[0].previousSibling
      ? $(this.placeholder[0].previousSibling)
      : null;
    if (previousItem != null) {
      while (
        !previousItem.is(this.options.listItemSelector) ||
        previousItem[0] == this.currentItem[0] ||
        previousItem[0] == this.helper[0]
      ) {
        if (previousItem[0].previousSibling) {
          previousItem = $(previousItem[0].previousSibling);
        } else {
          previousItem = null;
          break;
        }
      }
    }
    // To find the next sibling in the list, keep stepping forward until we hit a valid list item.
    var nextItem = this.placeholder[0].nextSibling
      ? $(this.placeholder[0].nextSibling)
      : null;
    if (nextItem != null) {
      while (
        !nextItem.is(this.options.listItemSelector) ||
        nextItem[0] == this.currentItem[0] ||
        nextItem[0] == this.helper[0]
      ) {
        if (nextItem[0].nextSibling) {
          nextItem = $(nextItem[0].nextSibling);
        } else {
          nextItem = null;
          break;
        }
      }
    }

    this.beyondMaxLevels = 0;

    // We will change this to the instance of the nested container if
    // appropriate, so that the appropriate context is applied to the
    // super _contactContainers prototype method
    var containerInstance = this;
    this.refreshPositions();

    // If the item is moved to the left, send it to its parent's level unless there are siblings below it.
    if (
      !o.fixedNestingDepth &&
      parentItem != null &&
      nextItem == null &&
      ((o.rtl &&
        this.positionAbs.left + this.helper.outerWidth() >
          parentItem.offset().left + parentItem.outerWidth()) ||
        (!o.rtl && this.positionAbs.left < parentItem.offset().left))
    ) {
      parentItem.after(this.placeholder[0]);
      containerInstance =
        parentItem.closest(o.containerElementSelector).data(this.widgetName) ||
        containerInstance;
      this._clearEmpty(parentItem[0]);
      this.refreshPositions();
      this._trigger("change", event, this._uiHash());
    }
    // If the item is below a sibling and is moved to the right, make it a child of that sibling.
    else if (
      !o.fixedNestingDepth &&
      previousItem != null &&
      !previousItem.is(".djn-no-drag,.djn-thead") &&
      ((o.rtl &&
        this.positionAbs.left + this.helper.outerWidth() <
          previousItem.offset().left + previousItem.outerWidth() - o.tabSize) ||
        (!o.rtl &&
          this.positionAbs.left > previousItem.offset().left + o.tabSize))
    ) {
      this._isAllowed(previousItem, level, level + childLevels);

      if (this.beyondMaxLevels > 0) {
        return $.ui.djnsortable.prototype._contactContainers.apply(
          this,
          arguments
        );
      }
      var $previousItemChildContainer;
      $previousItemChildContainer = previousItem
        .nearest(o.containerElementSelector)
        .first();

      if (
        !$previousItemChildContainer.length &&
        !previousItem.closest(o.nestedContainerSelector).length
      ) {
        $previousItemChildContainer = this.options.createContainerElement(
          previousItem[0]
        );
        previousItem.append($previousItemChildContainer);
      }
      if ($previousItemChildContainer.length) {
        $previousItemChildContainer.append(this.placeholder);
        containerInstance = $previousItemChildContainer.data(this.widgetName);
        if (!containerInstance) {
          containerInstance = createChildNestedSortable(
            this,
            $previousItemChildContainer[0]
          );
        }
        this.refreshPositions();
      }
      this._trigger("change", event, this._uiHash());
    } else {
      this._isAllowed(parentItem, level, level + childLevels);
    }

    $.ui.djnsortable.prototype._contactContainers.call(this, event);
  },

  _rearrange: function _rearrange(event, item, a, hardRefresh) {
    // Cache the rearranged element for the call to _clear()
    var o = this.options;
    if (item && typeof item == "object" && item.item) {
      this.lastRearrangedElement = item.item[0];
    }
    if (
      item &&
      typeof item == "object" &&
      item.item &&
      this.placeholder.closest(o.nestedContainerSelector).length
    ) {
      // This means we have been dropped into a nested container down a level
      // from the parent.
      var placeholderParentItem = this.placeholder.closest(o.listItemSelector);
      var comparisonElement =
        this.direction == "down"
          ? placeholderParentItem.next(o.nestedContainerSelector)
          : placeholderParentItem;
      if (comparisonElement.length && comparisonElement[0] == item.item[0]) {
        //Various things done here to improve the performance:
        // 1. we create a setTimeout, that calls refreshPositions
        // 2. on the instance, we have a counter variable, that get's higher after every append
        // 3. on the local scope, we copy the counter variable, and check in the timeout, if it's still the same
        // 4. this lets only the last addition to the timeout stack through
        this.counter = this.counter ? ++this.counter : 1;
        var counter = this.counter;

        this._delay(function () {
          if (counter == this.counter) this.refreshPositions(!hardRefresh); //Precompute after each DOM insertion, NOT on mousemove
        });
        // The super method will pop the container out of its nested container,
        // which we don't want.
        return;
      }
    }
    $.ui.djnsortable.prototype._rearrange.apply(this, arguments);
  },

  _convertPositionTo: function (d, pos) {
    // Cache the top offset before rearrangement
    this.previousTopOffset = this.placeholder.offset().top;
    return $.ui.djnsortable.prototype._convertPositionTo.apply(this, arguments);
  },

  _clear: function () {
    $.ui.djnsortable.prototype._clear.apply(this, arguments);
    // If lastRearrangedElement exists and is still attached to the document
    // (i.e., hasn't been removed)
    if (
      typeof this.lastRearrangedElement == "object" &&
      this.lastRearrangedElement.ownerDocument
    ) {
      this._clearEmpty(this.lastRearrangedElement);
    }
  },

  _mouseStop: function _mouseStop(event, noPropagation) {
    // If the item is in a position not allowed, send it back
    if (this.beyondMaxLevels) {
      this.placeholder.removeClass(this.options.errorClass);

      if (this.domPosition.prev) {
        $(this.domPosition.prev).after(this.placeholder);
      } else {
        $(this.domPosition.parent).prepend(this.placeholder);
      }
      this._trigger("revert", event, this._uiHash());
    }

    // Clean last empty container/list item
    for (var i = this.items.length - 1; i >= 0; i--) {
      var item = this.items[i].item[0];
      this._clearEmpty(item);
    }

    $.ui.djnsortable.prototype._mouseStop.apply(this, arguments);
  },

  toArray: function (o) {
    o = $.extend(true, {}, this.options, o || {});

    var sDepth = o.startDepthCount || 0,
      ret = [],
      left = 2;

    ret.push({
      item_id: o.rootID,
      parent_id: "none",
      depth: sDepth,
      left: "1",
      right: ($(o.listItemSelector, this.element).length + 1) * 2,
    });

    var _recursiveArray = function (item, depth, left) {
      var right = left + 1,
        id,
        pid;

      var $childItems = $(item)
        .children(o.containerElementSelector)
        .find(o.items);

      if ($childItems.length > 0) {
        depth++;
        $childItems.each(function () {
          right = _recursiveArray($(this), depth, right);
        });
        depth--;
      }

      id = $(item)
        .attr(o.attribute || "id")
        .match(o.expression || /(.+)[-=_](.+)/);

      if (depth === sDepth + 1) {
        pid = o.rootID;
      } else {
        var parentItem = $(item)
          .parent(o.containerElementSelector)
          .parent(o.items)
          .attr(o.attribute || "id")
          .match(o.expression || /(.+)[-=_](.+)/);
        pid = parentItem[2];
      }

      if (id) {
        ret.push({
          item_id: id[2],
          parent_id: pid,
          depth: depth,
          left: left,
          right: right,
        });
      }

      left = right + 1;
      return left;
    };

    $(this.element)
      .children(o.listItemSelector)
      .each(function () {
        left = _recursiveArray(this, sDepth + 1, left);
      });

    ret = ret.sort(function (a, b) {
      return a.left - b.left;
    });

    return ret;
  },

  _clearEmpty: function (item) {
    if (this.options.doNotClear) {
      return;
    }
    var $item = $(item);
    var childContainers = $item.nearest(this.options.containerElementSelector);
    childContainers.each(function (i, childContainer) {
      var $childContainer = $(childContainer);
      if (!$childContainer.children().length) {
        var instance = $childContainer.data(this.widgetName);
        if (typeof instance == "object" && instance.destroy) {
          instance.destroy();
        }
        $childContainer.remove();
      }
    });
    if (!$item.children().length) {
      $item.remove();
    }
  },

  _getLevel: function (item) {
    var level = 1,
      o = this.options,
      list;

    if (o.containerElementSelector) {
      list = item.closest(o.containerElementSelector);
      while (list && list.length > 0 && !list.parent().is(".djn-group-root")) {
        // if (!list.is(o.nestedContainerSelector)) {
        level++;
        // }
        list = list.parent().closest(o.containerElementSelector);
      }
    }

    return level;
  },

  _getChildLevels: function (parent, depth) {
    var self = this,
      o = this.options,
      result = 0;
    depth = depth || 0;

    $(parent)
      .nearest(o.containerElementSelector)
      .first()
      .find(o.items)
      .each(function (index, child) {
        if ($(child).is(".djn-no-drag,.djn-thead")) {
          return;
        }
        result = Math.max(self._getChildLevels(child, depth + 1), result);
      });

    return depth ? result + 1 : result;
  },

  _isAllowed: function _isAllowed(parentItem, level, levels) {
    var o = this.options,
      isRoot = $(this.domPosition.parent).hasClass("ui-sortable")
        ? true
        : false;
    // this takes into account the maxLevels set to the recipient list
    // var maxLevels = this.placeholder.closest('.ui-sortable').nestedSortable('option', 'maxLevels');
    var maxLevels = o.maxLevels;

    // Is the root protected?
    // Are we trying to nest under a no-nest?
    // Are we nesting too deep?
    if (
      parentItem &&
      typeof parentItem == "object" &&
      typeof parentItem.selector == "undefined"
    ) {
      parentItem = $(parentItem);
    }

    if (
      !o.isAllowed.call(this, this.currentItem, parentItem, this.placeholder) ||
      (parentItem && parentItem.hasClass(o.disableNesting)) ||
      (o.protectRoot &&
        ((parentItem == null && !isRoot) || (isRoot && level > 1)))
    ) {
      this.placeholder.addClass(o.errorClass);
      if (maxLevels < levels && maxLevels != 0) {
        this.beyondMaxLevels = levels - maxLevels;
      } else {
        this.beyondMaxLevels = 1;
      }
    } else {
      if (maxLevels < levels && maxLevels != 0) {
        this.placeholder.addClass(o.errorClass);
        this.beyondMaxLevels = levels - maxLevels;
      } else {
        this.placeholder.removeClass(o.errorClass);
        this.beyondMaxLevels = 0;
      }
    }
  },

  _connectWith: function _connectWith() {
    var origConnectWith = $.ui.djnsortable.prototype._connectWith.apply(
        this,
        arguments
      ),
      connectWith = [];
    var self = this;
    for (var i = 0; i < origConnectWith.length; i++) {
      var $elements = $(origConnectWith[i]);
      $elements.each(function (j, el) {
        if (el == self.element[0]) {
          return;
        }
        if (!self.options.canConnectWith(self.element, $(el), self)) {
          return;
        }
        connectWith.push(el);
      });
    }
    return connectWith;
  },
  _removeCurrentsFromItems: function () {
    var list = this.currentItem.find(":data(sortable-item)");
    for (var i = 0; i < this.items.length; i++) {
      for (var j = 0; j < list.length; j++) {
        if (list[j] == this.items[i].item[0]) {
          this.items.splice(i, 1);
          if (i >= this.items.length) {
            break;
          }
        }
      }
    }
  },
  createContainerElement: function (parent) {
    if (!parent.childNodes) {
      throw new Error(
        "Invalid element 'parent' passed to " + "createContainerElement."
      );
    }
    var newContainer = this.options.createContainerElement.apply(
      this,
      arguments
    );
    parent.appendChild(newContainer[0]);
    return $(newContainer);
  },
});

$.ui.nestedSortable.prototype.options = $.extend(
  {},
  $.ui.djnsortable.prototype.options,
  $.ui.nestedSortable.prototype.options
);
