import $ from "jquery";
/*!
 * jQuery UI Sortable @VERSION
 * http://jqueryui.com
 *
 * Copyright 2012 jQuery Foundation and other contributors
 * Released under the MIT license.
 * http://jquery.org/license
 *
 * http://api.jqueryui.com/sortable/
 *
 * Depends:
 *	jquery.ui.core.js
 *	jquery.ui.mouse.js
 *	jquery.ui.widget.js
 */
if ($.ui === undefined) {
  var jQuery = $;
  /* eslint-disable */
    (function(e,t){function i(t,i){var s,n,r,o=t.nodeName.toLowerCase();return"area"===o?(s=t.parentNode,n=s.name,t.href&&n&&"map"===s.nodeName.toLowerCase()?(r=e("img[usemap=#"+n+"]")[0],!!r&&a(r)):!1):(/input|select|textarea|button|object/.test(o)?!t.disabled:"a"===o?t.href||i:i)&&a(t)}function a(t){return e.expr.filters.visible(t)&&!e(t).parents().addBack().filter(function(){return"hidden"===e.css(this,"visibility")}).length}var s=0,n=/^ui-id-\d+$/;e.ui=e.ui||{},e.extend(e.ui,{version:"1.10.3",keyCode:{BACKSPACE:8,COMMA:188,DELETE:46,DOWN:40,END:35,ENTER:13,ESCAPE:27,HOME:36,LEFT:37,NUMPAD_ADD:107,NUMPAD_DECIMAL:110,NUMPAD_DIVIDE:111,NUMPAD_ENTER:108,NUMPAD_MULTIPLY:106,NUMPAD_SUBTRACT:109,PAGE_DOWN:34,PAGE_UP:33,PERIOD:190,RIGHT:39,SPACE:32,TAB:9,UP:38}}),e.fn.extend({focus:function(t){return function(i,a){return"number"==typeof i?this.each(function(){var t=this;setTimeout(function(){e(t).focus(),a&&a.call(t)},i)}):t.apply(this,arguments)}}(e.fn.focus),scrollParent:function(){var t;return t=e.ui.ie&&/(static|relative)/.test(this.css("position"))||/absolute/.test(this.css("position"))?this.parents().filter(function(){return/(relative|absolute|fixed)/.test(e.css(this,"position"))&&/(auto|scroll)/.test(e.css(this,"overflow")+e.css(this,"overflow-y")+e.css(this,"overflow-x"))}).eq(0):this.parents().filter(function(){return/(auto|scroll)/.test(e.css(this,"overflow")+e.css(this,"overflow-y")+e.css(this,"overflow-x"))}).eq(0),/fixed/.test(this.css("position"))||!t.length?e(document):t},zIndex:function(i){if(i!==t)return this.css("zIndex",i);if(this.length)for(var a,s,n=e(this[0]);n.length&&n[0]!==document;){if(a=n.css("position"),("absolute"===a||"relative"===a||"fixed"===a)&&(s=parseInt(n.css("zIndex"),10),!isNaN(s)&&0!==s))return s;n=n.parent()}return 0},uniqueId:function(){return this.each(function(){this.id||(this.id="ui-id-"+ ++s)})},removeUniqueId:function(){return this.each(function(){n.test(this.id)&&e(this).removeAttr("id")})}}),e.extend(e.expr[":"],{data:e.expr.createPseudo?e.expr.createPseudo(function(t){return function(i){return!!e.data(i,t)}}):function(t,i,a){return!!e.data(t,a[3])},focusable:function(t){return i(t,!isNaN(e.attr(t,"tabindex")))},tabbable:function(t){var a=e.attr(t,"tabindex"),s=isNaN(a);return(s||a>=0)&&i(t,!s)}}),e("<a>").outerWidth(1).jquery||e.each(["Width","Height"],function(i,a){function s(t,i,a,s){return e.each(n,function(){i-=parseFloat(e.css(t,"padding"+this))||0,a&&(i-=parseFloat(e.css(t,"border"+this+"Width"))||0),s&&(i-=parseFloat(e.css(t,"margin"+this))||0)}),i}var n="Width"===a?["Left","Right"]:["Top","Bottom"],r=a.toLowerCase(),o={innerWidth:e.fn.innerWidth,innerHeight:e.fn.innerHeight,outerWidth:e.fn.outerWidth,outerHeight:e.fn.outerHeight};e.fn["inner"+a]=function(i){return i===t?o["inner"+a].call(this):this.each(function(){e(this).css(r,s(this,i)+"px")})},e.fn["outer"+a]=function(t,i){return"number"!=typeof t?o["outer"+a].call(this,t):this.each(function(){e(this).css(r,s(this,t,!0,i)+"px")})}}),e.fn.addBack||(e.fn.addBack=function(e){return this.add(null==e?this.prevObject:this.prevObject.filter(e))}),e("<a>").data("a-b","a").removeData("a-b").data("a-b")&&(e.fn.removeData=function(t){return function(i){return arguments.length?t.call(this,e.camelCase(i)):t.call(this)}}(e.fn.removeData)),e.ui.ie=!!/msie [\w.]+/.exec(navigator.userAgent.toLowerCase()),e.support.selectstart="onselectstart"in document.createElement("div"),e.fn.extend({disableSelection:function(){return this.bind((e.support.selectstart?"selectstart":"mousedown")+".ui-disableSelection",function(e){e.preventDefault()})},enableSelection:function(){return this.unbind(".ui-disableSelection")}}),e.extend(e.ui,{plugin:{add:function(t,i,a){var s,n=e.ui[t].prototype;for(s in a)n.plugins[s]=n.plugins[s]||[],n.plugins[s].push([i,a[s]])},call:function(e,t,i){var a,s=e.plugins[t];if(s&&e.element[0].parentNode&&11!==e.element[0].parentNode.nodeType)for(a=0;s.length>a;a++)e.options[s[a][0]]&&s[a][1].apply(e.element,i)}},hasScroll:function(t,i){if("hidden"===e(t).css("overflow"))return!1;var a=i&&"left"===i?"scrollLeft":"scrollTop",s=!1;return t[a]>0?!0:(t[a]=1,s=t[a]>0,t[a]=0,s)}})})(jQuery);(function(e,t){var i=0,s=Array.prototype.slice,a=e.cleanData;e.cleanData=function(t){for(var i,s=0;null!=(i=t[s]);s++)try{e(i).triggerHandler("remove")}catch(n){}a(t)},e.widget=function(i,s,a){var n,r,o,h,l={},u=i.split(".")[0];i=i.split(".")[1],n=u+"-"+i,a||(a=s,s=e.Widget),e.expr[":"][n.toLowerCase()]=function(t){return!!e.data(t,n)},e[u]=e[u]||{},r=e[u][i],o=e[u][i]=function(e,i){return this._createWidget?(arguments.length&&this._createWidget(e,i),t):new o(e,i)},e.extend(o,r,{version:a.version,_proto:e.extend({},a),_childConstructors:[]}),h=new s,h.options=e.widget.extend({},h.options),e.each(a,function(i,a){return e.isFunction(a)?(l[i]=function(){var e=function(){return s.prototype[i].apply(this,arguments)},t=function(e){return s.prototype[i].apply(this,e)};return function(){var i,s=this._super,n=this._superApply;return this._super=e,this._superApply=t,i=a.apply(this,arguments),this._super=s,this._superApply=n,i}}(),t):(l[i]=a,t)}),o.prototype=e.widget.extend(h,{widgetEventPrefix:r?h.widgetEventPrefix:i},l,{constructor:o,namespace:u,widgetName:i,widgetFullName:n}),r?(e.each(r._childConstructors,function(t,i){var s=i.prototype;e.widget(s.namespace+"."+s.widgetName,o,i._proto)}),delete r._childConstructors):s._childConstructors.push(o),e.widget.bridge(i,o)},e.widget.extend=function(i){for(var a,n,r=s.call(arguments,1),o=0,h=r.length;h>o;o++)for(a in r[o])n=r[o][a],r[o].hasOwnProperty(a)&&n!==t&&(i[a]=e.isPlainObject(n)?e.isPlainObject(i[a])?e.widget.extend({},i[a],n):e.widget.extend({},n):n);return i},e.widget.bridge=function(i,a){var n=a.prototype.widgetFullName||i;e.fn[i]=function(r){var o="string"==typeof r,h=s.call(arguments,1),l=this;return r=!o&&h.length?e.widget.extend.apply(null,[r].concat(h)):r,o?this.each(function(){var s,a=e.data(this,n);return a?e.isFunction(a[r])&&"_"!==r.charAt(0)?(s=a[r].apply(a,h),s!==a&&s!==t?(l=s&&s.jquery?l.pushStack(s.get()):s,!1):t):e.error("no such method '"+r+"' for "+i+" widget instance"):e.error("cannot call methods on "+i+" prior to initialization; "+"attempted to call method '"+r+"'")}):this.each(function(){var t=e.data(this,n);t?t.option(r||{})._init():e.data(this,n,new a(r,this))}),l}},e.Widget=function(){},e.Widget._childConstructors=[],e.Widget.prototype={widgetName:"widget",widgetEventPrefix:"",defaultElement:"<div>",options:{disabled:!1,create:null},_createWidget:function(t,s){s=e(s||this.defaultElement||this)[0],this.element=e(s),this.uuid=i++,this.eventNamespace="."+this.widgetName+this.uuid,this.options=e.widget.extend({},this.options,this._getCreateOptions(),t),this.bindings=e(),this.hoverable=e(),this.focusable=e(),s!==this&&(e.data(s,this.widgetFullName,this),this._on(!0,this.element,{remove:function(e){e.target===s&&this.destroy()}}),this.document=e(s.style?s.ownerDocument:s.document||s),this.window=e(this.document[0].defaultView||this.document[0].parentWindow)),this._create(),this._trigger("create",null,this._getCreateEventData()),this._init()},_getCreateOptions:e.noop,_getCreateEventData:e.noop,_create:e.noop,_init:e.noop,destroy:function(){this._destroy(),this.element.unbind(this.eventNamespace).removeData(this.widgetName).removeData(this.widgetFullName).removeData(e.camelCase(this.widgetFullName)),this.widget().unbind(this.eventNamespace).removeAttr("aria-disabled").removeClass(this.widgetFullName+"-disabled "+"ui-state-disabled"),this.bindings.unbind(this.eventNamespace),this.hoverable.removeClass("ui-state-hover"),this.focusable.removeClass("ui-state-focus")},_destroy:e.noop,widget:function(){return this.element},option:function(i,s){var a,n,r,o=i;if(0===arguments.length)return e.widget.extend({},this.options);if("string"==typeof i)if(o={},a=i.split("."),i=a.shift(),a.length){for(n=o[i]=e.widget.extend({},this.options[i]),r=0;a.length-1>r;r++)n[a[r]]=n[a[r]]||{},n=n[a[r]];if(i=a.pop(),s===t)return n[i]===t?null:n[i];n[i]=s}else{if(s===t)return this.options[i]===t?null:this.options[i];o[i]=s}return this._setOptions(o),this},_setOptions:function(e){var t;for(t in e)this._setOption(t,e[t]);return this},_setOption:function(e,t){return this.options[e]=t,"disabled"===e&&(this.widget().toggleClass(this.widgetFullName+"-disabled ui-state-disabled",!!t).attr("aria-disabled",t),this.hoverable.removeClass("ui-state-hover"),this.focusable.removeClass("ui-state-focus")),this},enable:function(){return this._setOption("disabled",!1)},disable:function(){return this._setOption("disabled",!0)},_on:function(i,s,a){var n,r=this;"boolean"!=typeof i&&(a=s,s=i,i=!1),a?(s=n=e(s),this.bindings=this.bindings.add(s)):(a=s,s=this.element,n=this.widget()),e.each(a,function(a,o){function h(){return i||r.options.disabled!==!0&&!e(this).hasClass("ui-state-disabled")?("string"==typeof o?r[o]:o).apply(r,arguments):t}"string"!=typeof o&&(h.guid=o.guid=o.guid||h.guid||e.guid++);var l=a.match(/^(\w+)\s*(.*)$/),u=l[1]+r.eventNamespace,c=l[2];c?n.delegate(c,u,h):s.bind(u,h)})},_off:function(e,t){t=(t||"").split(" ").join(this.eventNamespace+" ")+this.eventNamespace,e.unbind(t).undelegate(t)},_delay:function(e,t){function i(){return("string"==typeof e?s[e]:e).apply(s,arguments)}var s=this;return setTimeout(i,t||0)},_hoverable:function(t){this.hoverable=this.hoverable.add(t),this._on(t,{mouseenter:function(t){e(t.currentTarget).addClass("ui-state-hover")},mouseleave:function(t){e(t.currentTarget).removeClass("ui-state-hover")}})},_focusable:function(t){this.focusable=this.focusable.add(t),this._on(t,{focusin:function(t){e(t.currentTarget).addClass("ui-state-focus")},focusout:function(t){e(t.currentTarget).removeClass("ui-state-focus")}})},_trigger:function(t,i,s){var a,n,r=this.options[t];if(s=s||{},i=e.Event(i),i.type=(t===this.widgetEventPrefix?t:this.widgetEventPrefix+t).toLowerCase(),i.target=this.element[0],n=i.originalEvent)for(a in n)a in i||(i[a]=n[a]);return this.element.trigger(i,s),!(e.isFunction(r)&&r.apply(this.element[0],[i].concat(s))===!1||i.isDefaultPrevented())}},e.each({show:"fadeIn",hide:"fadeOut"},function(t,i){e.Widget.prototype["_"+t]=function(s,a,n){"string"==typeof a&&(a={effect:a});var r,o=a?a===!0||"number"==typeof a?i:a.effect||i:t;a=a||{},"number"==typeof a&&(a={duration:a}),r=!e.isEmptyObject(a),a.complete=n,a.delay&&s.delay(a.delay),r&&e.effects&&e.effects.effect[o]?s[t](a):o!==t&&s[o]?s[o](a.duration,a.easing,n):s.queue(function(i){e(this)[t](),n&&n.call(s[0]),i()})}})})(jQuery);(function(e){var t=!1;e(document).mouseup(function(){t=!1}),e.widget("ui.mouse",{version:"1.10.3",options:{cancel:"input,textarea,button,select,option",distance:1,delay:0},_mouseInit:function(){var t=this;this.element.bind("mousedown."+this.widgetName,function(e){return t._mouseDown(e)}).bind("click."+this.widgetName,function(i){return!0===e.data(i.target,t.widgetName+".preventClickEvent")?(e.removeData(i.target,t.widgetName+".preventClickEvent"),i.stopImmediatePropagation(),!1):undefined}),this.started=!1},_mouseDestroy:function(){this.element.unbind("."+this.widgetName),this._mouseMoveDelegate&&e(document).unbind("mousemove."+this.widgetName,this._mouseMoveDelegate).unbind("mouseup."+this.widgetName,this._mouseUpDelegate)},_mouseDown:function(i){if(!t){this._mouseStarted&&this._mouseUp(i),this._mouseDownEvent=i;var s=this,a=1===i.which,n="string"==typeof this.options.cancel&&i.target.nodeName?e(i.target).closest(this.options.cancel).length:!1;return a&&!n&&this._mouseCapture(i)?(this.mouseDelayMet=!this.options.delay,this.mouseDelayMet||(this._mouseDelayTimer=setTimeout(function(){s.mouseDelayMet=!0},this.options.delay)),this._mouseDistanceMet(i)&&this._mouseDelayMet(i)&&(this._mouseStarted=this._mouseStart(i)!==!1,!this._mouseStarted)?(i.preventDefault(),!0):(!0===e.data(i.target,this.widgetName+".preventClickEvent")&&e.removeData(i.target,this.widgetName+".preventClickEvent"),this._mouseMoveDelegate=function(e){return s._mouseMove(e)},this._mouseUpDelegate=function(e){return s._mouseUp(e)},e(document).bind("mousemove."+this.widgetName,this._mouseMoveDelegate).bind("mouseup."+this.widgetName,this._mouseUpDelegate),i.preventDefault(),t=!0,!0)):!0}},_mouseMove:function(t){return e.ui.ie&&(!document.documentMode||9>document.documentMode)&&!t.button?this._mouseUp(t):this._mouseStarted?(this._mouseDrag(t),t.preventDefault()):(this._mouseDistanceMet(t)&&this._mouseDelayMet(t)&&(this._mouseStarted=this._mouseStart(this._mouseDownEvent,t)!==!1,this._mouseStarted?this._mouseDrag(t):this._mouseUp(t)),!this._mouseStarted)},_mouseUp:function(t){return e(document).unbind("mousemove."+this.widgetName,this._mouseMoveDelegate).unbind("mouseup."+this.widgetName,this._mouseUpDelegate),this._mouseStarted&&(this._mouseStarted=!1,t.target===this._mouseDownEvent.target&&e.data(t.target,this.widgetName+".preventClickEvent",!0),this._mouseStop(t)),!1},_mouseDistanceMet:function(e){return Math.max(Math.abs(this._mouseDownEvent.pageX-e.pageX),Math.abs(this._mouseDownEvent.pageY-e.pageY))>=this.options.distance},_mouseDelayMet:function(){return this.mouseDelayMet},_mouseStart:function(){},_mouseDrag:function(){},_mouseStop:function(){},_mouseCapture:function(){return!0}})})(jQuery);(function(e,t){function i(e,t,i){return[parseFloat(e[0])*(p.test(e[0])?t/100:1),parseFloat(e[1])*(p.test(e[1])?i/100:1)]}function s(t,i){return parseInt(e.css(t,i),10)||0}function a(t){var i=t[0];return 9===i.nodeType?{width:t.width(),height:t.height(),offset:{top:0,left:0}}:e.isWindow(i)?{width:t.width(),height:t.height(),offset:{top:t.scrollTop(),left:t.scrollLeft()}}:i.preventDefault?{width:0,height:0,offset:{top:i.pageY,left:i.pageX}}:{width:t.outerWidth(),height:t.outerHeight(),offset:t.offset()}}e.ui=e.ui||{};var n,r=Math.max,o=Math.abs,h=Math.round,l=/left|center|right/,u=/top|center|bottom/,c=/[\+\-]\d+(\.[\d]+)?%?/,d=/^\w+/,p=/%$/,f=e.fn.position;e.position={scrollbarWidth:function(){if(n!==t)return n;var i,s,a=e("<div style='display:block;width:50px;height:50px;overflow:hidden;'><div style='height:100px;width:auto;'></div></div>"),r=a.children()[0];return e("body").append(a),i=r.offsetWidth,a.css("overflow","scroll"),s=r.offsetWidth,i===s&&(s=a[0].clientWidth),a.remove(),n=i-s},getScrollInfo:function(t){var i=t.isWindow?"":t.element.css("overflow-x"),s=t.isWindow?"":t.element.css("overflow-y"),a="scroll"===i||"auto"===i&&t.width<t.element[0].scrollWidth,n="scroll"===s||"auto"===s&&t.height<t.element[0].scrollHeight;return{width:n?e.position.scrollbarWidth():0,height:a?e.position.scrollbarWidth():0}},getWithinInfo:function(t){var i=e(t||window),s=e.isWindow(i[0]);return{element:i,isWindow:s,offset:i.offset()||{left:0,top:0},scrollLeft:i.scrollLeft(),scrollTop:i.scrollTop(),width:s?i.width():i.outerWidth(),height:s?i.height():i.outerHeight()}}},e.fn.position=function(t){if(!t||!t.of)return f.apply(this,arguments);t=e.extend({},t);var n,p,m,g,v,y,b=e(t.of),_=e.position.getWithinInfo(t.within),x=e.position.getScrollInfo(_),k=(t.collision||"flip").split(" "),w={};return y=a(b),b[0].preventDefault&&(t.at="left top"),p=y.width,m=y.height,g=y.offset,v=e.extend({},g),e.each(["my","at"],function(){var e,i,s=(t[this]||"").split(" ");1===s.length&&(s=l.test(s[0])?s.concat(["center"]):u.test(s[0])?["center"].concat(s):["center","center"]),s[0]=l.test(s[0])?s[0]:"center",s[1]=u.test(s[1])?s[1]:"center",e=c.exec(s[0]),i=c.exec(s[1]),w[this]=[e?e[0]:0,i?i[0]:0],t[this]=[d.exec(s[0])[0],d.exec(s[1])[0]]}),1===k.length&&(k[1]=k[0]),"right"===t.at[0]?v.left+=p:"center"===t.at[0]&&(v.left+=p/2),"bottom"===t.at[1]?v.top+=m:"center"===t.at[1]&&(v.top+=m/2),n=i(w.at,p,m),v.left+=n[0],v.top+=n[1],this.each(function(){var a,l,u=e(this),c=u.outerWidth(),d=u.outerHeight(),f=s(this,"marginLeft"),y=s(this,"marginTop"),D=c+f+s(this,"marginRight")+x.width,T=d+y+s(this,"marginBottom")+x.height,M=e.extend({},v),S=i(w.my,u.outerWidth(),u.outerHeight());"right"===t.my[0]?M.left-=c:"center"===t.my[0]&&(M.left-=c/2),"bottom"===t.my[1]?M.top-=d:"center"===t.my[1]&&(M.top-=d/2),M.left+=S[0],M.top+=S[1],e.support.offsetFractions||(M.left=h(M.left),M.top=h(M.top)),a={marginLeft:f,marginTop:y},e.each(["left","top"],function(i,s){e.ui.position[k[i]]&&e.ui.position[k[i]][s](M,{targetWidth:p,targetHeight:m,elemWidth:c,elemHeight:d,collisionPosition:a,collisionWidth:D,collisionHeight:T,offset:[n[0]+S[0],n[1]+S[1]],my:t.my,at:t.at,within:_,elem:u})}),t.using&&(l=function(e){var i=g.left-M.left,s=i+p-c,a=g.top-M.top,n=a+m-d,h={target:{element:b,left:g.left,top:g.top,width:p,height:m},element:{element:u,left:M.left,top:M.top,width:c,height:d},horizontal:0>s?"left":i>0?"right":"center",vertical:0>n?"top":a>0?"bottom":"middle"};c>p&&p>o(i+s)&&(h.horizontal="center"),d>m&&m>o(a+n)&&(h.vertical="middle"),h.important=r(o(i),o(s))>r(o(a),o(n))?"horizontal":"vertical",t.using.call(this,e,h)}),u.offset(e.extend(M,{using:l}))})},e.ui.position={fit:{left:function(e,t){var i,s=t.within,a=s.isWindow?s.scrollLeft:s.offset.left,n=s.width,o=e.left-t.collisionPosition.marginLeft,h=a-o,l=o+t.collisionWidth-n-a;t.collisionWidth>n?h>0&&0>=l?(i=e.left+h+t.collisionWidth-n-a,e.left+=h-i):e.left=l>0&&0>=h?a:h>l?a+n-t.collisionWidth:a:h>0?e.left+=h:l>0?e.left-=l:e.left=r(e.left-o,e.left)},top:function(e,t){var i,s=t.within,a=s.isWindow?s.scrollTop:s.offset.top,n=t.within.height,o=e.top-t.collisionPosition.marginTop,h=a-o,l=o+t.collisionHeight-n-a;t.collisionHeight>n?h>0&&0>=l?(i=e.top+h+t.collisionHeight-n-a,e.top+=h-i):e.top=l>0&&0>=h?a:h>l?a+n-t.collisionHeight:a:h>0?e.top+=h:l>0?e.top-=l:e.top=r(e.top-o,e.top)}},flip:{left:function(e,t){var i,s,a=t.within,n=a.offset.left+a.scrollLeft,r=a.width,h=a.isWindow?a.scrollLeft:a.offset.left,l=e.left-t.collisionPosition.marginLeft,u=l-h,c=l+t.collisionWidth-r-h,d="left"===t.my[0]?-t.elemWidth:"right"===t.my[0]?t.elemWidth:0,p="left"===t.at[0]?t.targetWidth:"right"===t.at[0]?-t.targetWidth:0,f=-2*t.offset[0];0>u?(i=e.left+d+p+f+t.collisionWidth-r-n,(0>i||o(u)>i)&&(e.left+=d+p+f)):c>0&&(s=e.left-t.collisionPosition.marginLeft+d+p+f-h,(s>0||c>o(s))&&(e.left+=d+p+f))},top:function(e,t){var i,s,a=t.within,n=a.offset.top+a.scrollTop,r=a.height,h=a.isWindow?a.scrollTop:a.offset.top,l=e.top-t.collisionPosition.marginTop,u=l-h,c=l+t.collisionHeight-r-h,d="top"===t.my[1],p=d?-t.elemHeight:"bottom"===t.my[1]?t.elemHeight:0,f="top"===t.at[1]?t.targetHeight:"bottom"===t.at[1]?-t.targetHeight:0,m=-2*t.offset[1];0>u?(s=e.top+p+f+m+t.collisionHeight-r-n,e.top+p+f+m>u&&(0>s||o(u)>s)&&(e.top+=p+f+m)):c>0&&(i=e.top-t.collisionPosition.marginTop+p+f+m-h,e.top+p+f+m>c&&(i>0||c>o(i))&&(e.top+=p+f+m))}},flipfit:{left:function(){e.ui.position.flip.left.apply(this,arguments),e.ui.position.fit.left.apply(this,arguments)},top:function(){e.ui.position.flip.top.apply(this,arguments),e.ui.position.fit.top.apply(this,arguments)}}},function(){var t,i,s,a,n,r=document.getElementsByTagName("body")[0],o=document.createElement("div");t=document.createElement(r?"div":"body"),s={visibility:"hidden",width:0,height:0,border:0,margin:0,background:"none"},r&&e.extend(s,{position:"absolute",left:"-1000px",top:"-1000px"});for(n in s)t.style[n]=s[n];t.appendChild(o),i=r||document.documentElement,i.insertBefore(t,i.firstChild),o.style.cssText="position: absolute; left: 10.7432222px;",a=e(o).offset().left,e.support.offsetFractions=a>10&&11>a,t.innerHTML="",i.removeChild(t)}()})(jQuery);
		/* eslint-enable */
}

$.widget("ui.djnsortable", $.ui.mouse, {
  version: "@VERSION",
  widgetEventPrefix: "sort",
  ready: false,
  options: {
    appendTo: "parent",
    axis: false,
    connectWith: false,
    containment: false,
    cursor: "auto",
    cursorAt: false,
    dropOnEmpty: true,
    forcePlaceholderSize: false,
    forceHelperSize: false,
    grid: false,
    handle: false,
    helper: "original",
    items: "> *",
    opacity: false,
    placeholder: false,
    revert: false,
    scroll: true,
    scrollSensitivity: 20,
    scrollSpeed: 20,
    scope: "default",
    tolerance: "intersect",
    zIndex: 1000,
  },

  _isOverAxis: function (x, reference, size) {
    return x >= reference && x < reference + size;
  },

  _create: function () {
    var o = this.options;
    this.containerCache = {};
    this.element.addClass("ui-sortable");

    //Get the items
    this.refresh();

    //Let's determine if the items are being displayed horizontally
    this.floating = this.items.length
      ? o.axis === "x" ||
        /left|right/.test(this.items[0].item.css("float")) ||
        /inline|table-cell/.test(this.items[0].item.css("display"))
      : false;

    //Let's determine the parent's offset
    this.offset = this.element.offset();

    //Initialize mouse events for interaction
    this._mouseInit();

    //We're ready to go
    this.ready = true;
  },

  _destroy: function () {
    this.element.removeClass("ui-sortable ui-sortable-disabled");
    this._mouseDestroy();

    for (var i = this.items.length - 1; i >= 0; i--)
      this.items[i].item.removeData(this.widgetName + "-item");

    return this;
  },

  _setOption: function (key, value) {
    if (key === "disabled") {
      this.options[key] = value;

      this.widget().toggleClass("ui-sortable-disabled", !!value);
    } else {
      // Don't call widget base _setOption for disable as it adds ui-state-disabled class
      $.Widget.prototype._setOption.apply(this, arguments);
    }
  },

  _mouseCapture: function (event, overrideHandle) {
    var that = this;

    if (this.reverting) {
      return false;
    }

    if (this.options.disabled || this.options.type == "static") return false;

    //We have to refresh the items data once first
    this._refreshItems(event);

    //Find out if the clicked node (or one of its parents) is a actual item in this.items
    var currentItem = null,
      nodes = $(event.target)
        .parents()
        .each(function () {
          if ($.data(this, that.widgetName + "-item") == that) {
            currentItem = $(this);
            return false;
          }
        });
    if ($.data(event.target, that.widgetName + "-item") == that)
      currentItem = $(event.target);

    if (!currentItem) return false;
    if (this.options.handle && !overrideHandle) {
      var validHandle = false;
      var addBackMethod = $.fn.addBack ? "addBack" : "andSelf";

      $(this.options.handle, currentItem)
        .find("*")
        [addBackMethod]()
        .each(function () {
          if (this == event.target) validHandle = true;
        });
      if (!validHandle) return false;
    }

    this.currentItem = currentItem;
    this._removeCurrentsFromItems();
    return true;
  },

  _mouseStart: function (event, overrideHandle, noActivation) {
    var o = this.options;
    this.currentContainer = this;

    //We only need to call refreshPositions, because the refreshItems call has been moved to mouseCapture
    this.refreshPositions();

    //Create and append the visible helper
    this.helper = this._createHelper(event);

    //Cache the helper size
    this._cacheHelperProportions();

    /*
     * - Position generation -
     * This block generates everything position related - it's the core of draggables.
     */

    //Cache the margins of the original element
    this._cacheMargins();

    //Get the next scrolling parent
    this.scrollParent = this.helper.scrollParent();

    //The element's absolute position on the page minus margins
    this.offset = this.currentItem.offset();
    this.offset = {
      top: this.offset.top - this.margins.top,
      left: this.offset.left - this.margins.left,
    };

    $.extend(this.offset, {
      click: {
        //Where the click happened, relative to the element
        left: event.pageX - this.offset.left,
        top: event.pageY - this.offset.top,
      },
      parent: this._getParentOffset(),
      relative: this._getRelativeOffset(), //This is a relative to absolute position minus the actual position calculation - only used for relative positioned helper
    });

    // Only after we got the offset, we can change the helper's position to absolute
    // TODO: Still need to figure out a way to make relative sorting possible
    this.helper.css("position", "absolute");
    this.cssPosition = this.helper.css("position");

    //Generate the original position
    this.originalPosition = this._generatePosition(event);
    this.originalPageX = event.pageX;
    this.originalPageY = event.pageY;

    //Adjust the mouse offset relative to the helper if 'cursorAt' is supplied
    o.cursorAt && this._adjustOffsetFromHelper(o.cursorAt);

    //Cache the former DOM position
    this.domPosition = {
      prev: this.currentItem.prev()[0],
      parent: this.currentItem.parent()[0],
    };

    //If the helper is not the original, hide the original so it's not playing any role during the drag, won't cause anything bad this way
    if (this.helper[0] != this.currentItem[0]) {
      this.currentItem.hide();
    }

    //Create the placeholder
    this._createPlaceholder();

    //Set a containment if given in the options
    if (o.containment) this._setContainment();

    if (o.cursor) {
      // cursor option
      if ($("body").css("cursor")) this._storedCursor = $("body").css("cursor");
      $("body").css("cursor", o.cursor);
    }

    if (o.opacity) {
      // opacity option
      if (this.helper.css("opacity"))
        this._storedOpacity = this.helper.css("opacity");
      this.helper.css("opacity", o.opacity);
    }

    if (o.zIndex) {
      // zIndex option
      if (this.helper.css("zIndex"))
        this._storedZIndex = this.helper.css("zIndex");
      this.helper.css("zIndex", o.zIndex);
    }

    //Prepare scrolling
    if (
      this.scrollParent[0] != document &&
      this.scrollParent[0].tagName != "HTML"
    )
      this.overflowOffset = this.scrollParent.offset();

    //Call callbacks
    this._trigger("start", event, this._uiHash());

    //Recache the helper size
    if (!this._preserveHelperProportions) this._cacheHelperProportions();

    //Post 'activate' events to possible containers
    if (!noActivation) {
      for (var i = this.containers.length - 1; i >= 0; i--) {
        this.containers[i]._trigger("activate", event, this._uiHash(this));
      }
    }

    //Prepare possible droppables
    if ($.ui.ddmanager) $.ui.ddmanager.current = this;

    if ($.ui.ddmanager && !o.dropBehaviour)
      $.ui.ddmanager.prepareOffsets(this, event);

    this.dragging = true;

    this.helper.addClass("ui-sortable-helper");
    this._mouseDrag(event); //Execute the drag once - this causes the helper not to be visible before getting its correct position
    return true;
  },

  _mouseDrag: function (event) {
    //Compute the helpers position
    this.position = this._generatePosition(event);
    this.positionAbs = this._convertPositionTo("absolute");

    if (!this.lastPositionAbs) {
      this.lastPositionAbs = this.positionAbs;
    }

    //Do scrolling
    if (this.options.scroll) {
      var o = this.options,
        scrolled = false;
      if (
        this.scrollParent[0] != document &&
        this.scrollParent[0].tagName != "HTML"
      ) {
        if (
          this.overflowOffset.top +
            this.scrollParent[0].offsetHeight -
            event.pageY <
          o.scrollSensitivity
        )
          this.scrollParent[0].scrollTop = scrolled =
            this.scrollParent[0].scrollTop + o.scrollSpeed;
        else if (event.pageY - this.overflowOffset.top < o.scrollSensitivity)
          this.scrollParent[0].scrollTop = scrolled =
            this.scrollParent[0].scrollTop - o.scrollSpeed;

        if (
          this.overflowOffset.left +
            this.scrollParent[0].offsetWidth -
            event.pageX <
          o.scrollSensitivity
        )
          this.scrollParent[0].scrollLeft = scrolled =
            this.scrollParent[0].scrollLeft + o.scrollSpeed;
        else if (event.pageX - this.overflowOffset.left < o.scrollSensitivity)
          this.scrollParent[0].scrollLeft = scrolled =
            this.scrollParent[0].scrollLeft - o.scrollSpeed;
      } else {
        if (event.pageY - $(document).scrollTop() < o.scrollSensitivity)
          scrolled = $(document).scrollTop(
            $(document).scrollTop() - o.scrollSpeed
          );
        else if (
          $(window).height() - (event.pageY - $(document).scrollTop()) <
          o.scrollSensitivity
        )
          scrolled = $(document).scrollTop(
            $(document).scrollTop() + o.scrollSpeed
          );

        if (event.pageX - $(document).scrollLeft() < o.scrollSensitivity)
          scrolled = $(document).scrollLeft(
            $(document).scrollLeft() - o.scrollSpeed
          );
        else if (
          $(window).width() - (event.pageX - $(document).scrollLeft()) <
          o.scrollSensitivity
        )
          scrolled = $(document).scrollLeft(
            $(document).scrollLeft() + o.scrollSpeed
          );
      }

      if (scrolled !== false && $.ui.ddmanager && !o.dropBehaviour)
        $.ui.ddmanager.prepareOffsets(this, event);
    }

    //Regenerate the absolute position used for position checks
    this.positionAbs = this._convertPositionTo("absolute");

    //Set the helper position
    if (!this.options.axis || this.options.axis != "y")
      this.helper[0].style.left = this.position.left + "px";
    if (!this.options.axis || this.options.axis != "x")
      this.helper[0].style.top = this.position.top + "px";

    //Rearrange
    for (var i = this.items.length - 1; i >= 0; i--) {
      //Cache variables and intersection, continue if no intersection
      var item = this.items[i],
        itemElement = item.item[0],
        intersection = this._intersectsWithPointer(item);
      if (!intersection) continue;

      // Only put the placeholder inside the current Container, skip all
      // items form other containers. This works because when moving
      // an item from one container to another the
      // currentContainer is switched before the placeholder is moved.
      //
      // Without this moving items in "sub-sortables" can cause the placeholder to jitter
      // beetween the outer and inner container.
      if (item.instance !== this.currentContainer) continue;

      if (
        itemElement != this.currentItem[0] && //cannot intersect with itself
        this.placeholder[intersection == 1 ? "next" : "prev"]()[0] !=
          itemElement && //no useless actions that have been done before
        !$.contains(this.placeholder[0], itemElement) && //no action if the item moved is the parent of the item checked
        (this.options.type == "semi-dynamic"
          ? !$.contains(this.element[0], itemElement)
          : true)
        //&& itemElement.parentNode == this.placeholder[0].parentNode // only rearrange items within the same container
      ) {
        this.direction = intersection == 1 ? "down" : "up";

        if (
          this.options.tolerance == "pointer" ||
          this._intersectsWithSides(item)
        ) {
          this._rearrange(event, item);
        } else {
          break;
        }

        this._trigger("change", event, this._uiHash());
        break;
      }
    }

    //Post events to containers
    this._contactContainers(event);

    //Interconnect with droppables
    if ($.ui.ddmanager) $.ui.ddmanager.drag(this, event);

    //Call callbacks
    this._trigger("sort", event, this._uiHash());

    this.lastPositionAbs = this.positionAbs;
    return false;
  },

  _mouseStop: function (event, noPropagation) {
    if (!event) return;

    //If we are using droppables, inform the manager about the drop
    if ($.ui.ddmanager && !this.options.dropBehaviour)
      $.ui.ddmanager.drop(this, event);

    if (this.options.revert) {
      var that = this;
      var cur = this.placeholder.offset();

      this.reverting = true;

      $(this.helper).animate(
        {
          left:
            cur.left -
            this.offset.parent.left -
            this.margins.left +
            (this.offsetParent[0] == document.body
              ? 0
              : this.offsetParent[0].scrollLeft),
          top:
            cur.top -
            this.offset.parent.top -
            this.margins.top +
            (this.offsetParent[0] == document.body
              ? 0
              : this.offsetParent[0].scrollTop),
        },
        parseInt(this.options.revert, 10) || 500,
        function () {
          that._clear(event);
        }
      );
    } else {
      this._clear(event, noPropagation);
    }

    return false;
  },

  cancel: function () {
    if (this.dragging) {
      this._mouseUp({ target: null });

      if (this.options.helper == "original")
        this.currentItem.css(this._storedCSS).removeClass("ui-sortable-helper");
      else this.currentItem.show();

      //Post deactivating events to containers
      for (var i = this.containers.length - 1; i >= 0; i--) {
        this.containers[i]._trigger("deactivate", null, this._uiHash(this));
        if (this.containers[i].containerCache.over) {
          this.containers[i]._trigger("out", null, this._uiHash(this));
          this.containers[i].containerCache.over = 0;
        }
      }
    }

    if (this.placeholder) {
      //$(this.placeholder[0]).remove(); would have been the jQuery way - unfortunately, it unbinds ALL events from the original node!
      if (this.placeholder[0].parentNode)
        this.placeholder[0].parentNode.removeChild(this.placeholder[0]);
      if (
        this.options.helper != "original" &&
        this.helper &&
        this.helper[0].parentNode
      )
        this.helper.remove();

      $.extend(this, {
        helper: null,
        dragging: false,
        reverting: false,
        _noFinalSort: null,
      });

      if (this.domPosition.prev) {
        $(this.domPosition.prev).after(this.currentItem);
      } else {
        $(this.domPosition.parent).prepend(this.currentItem);
      }
    }

    return this;
  },

  serialize: function (o) {
    var items = this._getItemsAsjQuery(o && o.connected);
    var str = [];
    o = o || {};

    $(items).each(function () {
      var res = ($(o.item || this).attr(o.attribute || "id") || "").match(
        o.expression || /(.+)[-=_](.+)/
      );
      if (res)
        str.push(
          (o.key || res[1] + "[]") +
            "=" +
            (o.key && o.expression ? res[1] : res[2])
        );
    });

    if (!str.length && o.key) {
      str.push(o.key + "=");
    }

    return str.join("&");
  },

  toArray: function (o) {
    var items = this._getItemsAsjQuery(o && o.connected);
    var ret = [];
    o = o || {};

    items.each(function () {
      ret.push($(o.item || this).attr(o.attribute || "id") || "");
    });
    return ret;
  },

  /* Be careful with the following core functions */
  _intersectsWith: function (item) {
    var x1 = this.positionAbs.left,
      x2 = x1 + this.helperProportions.width,
      y1 = this.positionAbs.top,
      y2 = y1 + this.helperProportions.height;

    var l = item.left,
      r = l + item.width,
      t = item.top,
      b = t + Math.max(10, item.height);

    var dyClick = this.offset.click.top,
      dxClick = this.offset.click.left;

    var isOverElement =
      y1 + dyClick > t &&
      y1 + dyClick < b &&
      x1 + dxClick > l &&
      x1 + dxClick < r;

    if (
      this.options.tolerance == "pointer" ||
      this.options.forcePointerForContainers ||
      (this.options.tolerance != "pointer" &&
        this.helperProportions[this.floating ? "width" : "height"] >
          item[this.floating ? "width" : "height"])
    ) {
      return isOverElement;
    } else {
      return (
        l < x1 + this.helperProportions.width / 2 && // Right Half
        x2 - this.helperProportions.width / 2 < r && // Left Half
        t < y1 + this.helperProportions.height / 2 && // Bottom Half
        y2 - this.helperProportions.height / 2 < b
      ); // Top Half
    }
  },

  _intersectsWithPointer: function (item) {
    var isOverElementHeight =
        this.options.axis === "x" ||
        this._isOverAxis(
          this.positionAbs.top + this.offset.click.top,
          item.top,
          Math.max(10, item.height)
        ),
      isOverElementWidth =
        this.options.axis === "y" ||
        this._isOverAxis(
          this.positionAbs.left + this.offset.click.left,
          item.left,
          item.width
        ),
      isOverElement = isOverElementHeight && isOverElementWidth,
      verticalDirection = this._getDragVerticalDirection(),
      horizontalDirection = this._getDragHorizontalDirection();

    if (!isOverElement) return false;

    return this.floating
      ? (horizontalDirection && horizontalDirection == "right") ||
        verticalDirection == "down"
        ? 2
        : 1
      : verticalDirection && (verticalDirection == "down" ? 2 : 1);
  },

  _intersectsWithSides: function (item) {
    var isOverBottomHalf = this._isOverAxis(
        this.positionAbs.top + this.offset.click.top,
        item.top + Math.max(10, item.height) / 2,
        Math.max(10, item.height)
      ),
      isOverRightHalf = this._isOverAxis(
        this.positionAbs.left + this.offset.click.left,
        item.left + item.width / 2,
        item.width
      ),
      verticalDirection = this._getDragVerticalDirection(),
      horizontalDirection = this._getDragHorizontalDirection();

    if (this.floating && horizontalDirection) {
      return (
        (horizontalDirection == "right" && isOverRightHalf) ||
        (horizontalDirection == "left" && !isOverRightHalf)
      );
    } else {
      return (
        verticalDirection &&
        ((verticalDirection == "down" && isOverBottomHalf) ||
          (verticalDirection == "up" && !isOverBottomHalf))
      );
    }
  },

  _getDragVerticalDirection: function () {
    var delta = this.positionAbs.top - this.lastPositionAbs.top;
    return delta != 0 && (delta > 0 ? "down" : "up");
  },

  _getDragHorizontalDirection: function () {
    var delta = this.positionAbs.left - this.lastPositionAbs.left;
    return delta != 0 && (delta > 0 ? "right" : "left");
  },

  refresh: function (event) {
    this._refreshItems(event);
    this.refreshPositions();
    return this;
  },

  _connectWith: function () {
    var options = this.options;
    return options.connectWith.constructor == String
      ? [options.connectWith]
      : options.connectWith;
  },

  _getItemsAsjQuery: function (connected) {
    var items = [];
    var queries = [];
    var connectWith = this._connectWith();

    if (connectWith && connected) {
      for (var i = connectWith.length - 1; i >= 0; i--) {
        var cur = $(connectWith[i]);
        for (var j = cur.length - 1; j >= 0; j--) {
          var inst = $.data(cur[j], this.widgetName);
          if (inst && inst != this && !inst.options.disabled) {
            queries.push([
              $.isFunction(inst.options.items)
                ? inst.options.items.call(inst.element)
                : $(inst.options.items, inst.element)
                    .not(".ui-sortable-helper")
                    .not(".ui-sortable-placeholder"),
              inst,
            ]);
          }
        }
      }
    }

    queries.push([
      $.isFunction(this.options.items)
        ? this.options.items.call(this.element, null, {
            options: this.options,
            item: this.currentItem,
          })
        : $(this.options.items, this.element)
            .not(".ui-sortable-helper")
            .not(".ui-sortable-placeholder"),
      this,
    ]);

    for (var i = queries.length - 1; i >= 0; i--) {
      queries[i][0].each(function () {
        items.push(this);
      });
    }

    return $(items);
  },

  _removeCurrentsFromItems: function () {
    var list = this.currentItem.find(":data(" + this.widgetName + "-item)");

    this.items = $.grep(this.items, function (item) {
      for (var j = 0; j < list.length; j++) {
        if (list[j] == item.item[0]) return false;
      }
      return true;
    });
  },

  _refreshItems: function (event) {
    this.items = [];
    this.containers = [this];
    var items = this.items;
    var queries = [
      [
        $.isFunction(this.options.items)
          ? this.options.items.call(this.element[0], event, {
              item: this.currentItem,
            })
          : $(this.options.items, this.element),
        this,
      ],
    ];
    var connectWith = this._connectWith();

    if (connectWith && this.ready) {
      //Shouldn't be run the first time through due to massive slow-down
      for (var i = connectWith.length - 1; i >= 0; i--) {
        var cur = $(connectWith[i]);
        for (var j = cur.length - 1; j >= 0; j--) {
          var inst = $.data(cur[j], this.widgetName);
          if (inst && inst != this && !inst.options.disabled) {
            queries.push([
              $.isFunction(inst.options.items)
                ? inst.options.items.call(inst.element[0], event, {
                    item: this.currentItem,
                  })
                : $(inst.options.items, inst.element),
              inst,
            ]);
            this.containers.push(inst);
          }
        }
      }
    }

    for (var i = queries.length - 1; i >= 0; i--) {
      var targetData = queries[i][1];
      var _queries = queries[i][0];

      for (var j = 0, queriesLength = _queries.length; j < queriesLength; j++) {
        var item = $(_queries[j]);

        item.data(this.widgetName + "-item", targetData); // Data for target checking (mouse manager)

        items.push({
          item: item,
          instance: targetData,
          width: 0,
          height: 0,
          left: 0,
          top: 0,
        });
      }
    }
  },

  refreshPositions: function (fast) {
    //This has to be redone because due to the item being moved out/into the offsetParent, the offsetParent's position will change
    if (this.offsetParent && this.helper) {
      this.offset.parent = this._getParentOffset();
    }

    for (var i = this.items.length - 1; i >= 0; i--) {
      var item = this.items[i];

      //We ignore calculating positions of all connected containers when we're not over them
      if (
        item.instance != this.currentContainer &&
        this.currentContainer &&
        item.item[0] != this.currentItem[0]
      )
        continue;

      var t = this.options.toleranceElement
        ? $(this.options.toleranceElement, item.item)
        : item.item;

      if (!fast) {
        item.width = t.outerWidth();
        item.height = t.outerHeight();
      }

      var p = t.offset();
      item.left = p.left;
      item.top = p.top;
    }

    if (this.options.custom && this.options.custom.refreshContainers) {
      this.options.custom.refreshContainers.call(this);
    } else {
      for (var i = this.containers.length - 1; i >= 0; i--) {
        var p = this.containers[i].element.offset();
        this.containers[i].containerCache.left = p.left;
        this.containers[i].containerCache.top = p.top;
        this.containers[i].containerCache.width =
          this.containers[i].element.outerWidth();
        this.containers[i].containerCache.height =
          this.containers[i].element.outerHeight();
      }
    }

    return this;
  },

  _createPlaceholder: function (that) {
    that = that || this;
    var o = that.options;

    if (!o.placeholder || o.placeholder.constructor == String) {
      var className = o.placeholder;
      o.placeholder = {
        element: function () {
          var el = $(document.createElement(that.currentItem[0].nodeName))
            .addClass(
              className ||
                that.currentItem[0].className + " ui-sortable-placeholder"
            )
            .removeClass("ui-sortable-helper")[0];

          if (!className) el.style.visibility = "hidden";

          return el;
        },
        update: function (container, p) {
          // 1. If a className is set as 'placeholder option, we don't force sizes - the class is responsible for that
          // 2. The option 'forcePlaceholderSize can be enabled to force it even if a class name is specified
          if (className && !o.forcePlaceholderSize) return;

          //If the element doesn't have a actual height by itself (without styles coming from a stylesheet), it receives the inline height from the dragged item
          if (!p.height()) {
            p.height(
              that.currentItem.innerHeight() -
                parseInt(that.currentItem.css("paddingTop") || 0, 10) -
                parseInt(that.currentItem.css("paddingBottom") || 0, 10)
            );
          }
          if (!p.width()) {
            p.width(
              that.currentItem.innerWidth() -
                parseInt(that.currentItem.css("paddingLeft") || 0, 10) -
                parseInt(that.currentItem.css("paddingRight") || 0, 10)
            );
          }
        },
      };
    }

    //Create the placeholder
    that.placeholder = $(
      o.placeholder.element.call(that.element, that.currentItem)
    );

    //Append it after the actual current item
    that.currentItem.after(that.placeholder);

    //Update the size of the placeholder (TODO: Logic to fuzzy, see line 316/317)
    o.placeholder.update(that, that.placeholder);
  },

  _contactContainers: function (event) {
    // get innermost container that intersects with item
    var innermostContainer = null,
      innermostIndex = null;

    for (var i = this.containers.length - 1; i >= 0; i--) {
      // never consider a container that's located within the item itself
      if ($.contains(this.currentItem[0], this.containers[i].element[0]))
        continue;

      if (this._intersectsWith(this.containers[i].containerCache)) {
        // if we've already found a container and it's more "inner" than this, then continue
        if (
          innermostContainer &&
          $.contains(
            this.containers[i].element[0],
            innermostContainer.element[0]
          )
        )
          continue;

        innermostContainer = this.containers[i];
        innermostIndex = i;
      } else {
        // container doesn't intersect. trigger "out" event if necessary
        if (this.containers[i].containerCache.over) {
          this.containers[i]._trigger("out", event, this._uiHash(this));
          this.containers[i].containerCache.over = 0;
        }
      }
    }

    // if no intersecting containers found, return
    if (!innermostContainer) return;

    // move the item into the container if it's not there already
    if (this.containers.length === 1) {
      this.containers[innermostIndex]._trigger(
        "over",
        event,
        this._uiHash(this)
      );
      this.containers[innermostIndex].containerCache.over = 1;
    } else {
      //When entering a new container, we will find the item with the least distance and append our item near it
      var dist = 10000;
      var itemWithLeastDistance = null;
      var posProperty = this.containers[innermostIndex].floating
        ? "left"
        : "top";
      var sizeProperty = this.containers[innermostIndex].floating
        ? "width"
        : "height";
      var base = this.positionAbs[posProperty] + this.offset.click[posProperty];
      for (var j = this.items.length - 1; j >= 0; j--) {
        if (
          !$.contains(
            this.containers[innermostIndex].element[0],
            this.items[j].item[0]
          )
        )
          continue;
        if (this.items[j].item[0] == this.currentItem[0]) continue;
        var cur = this.items[j].item.offset()[posProperty];
        var nearBottom = false;
        if (
          Math.abs(cur - base) >
          Math.abs(cur + Math.max(10, this.items[j][sizeProperty]) - base)
        ) {
          nearBottom = true;
          cur += this.items[j][sizeProperty];
        }

        if (Math.abs(cur - base) < dist) {
          dist = Math.abs(cur - base);
          itemWithLeastDistance = this.items[j];
          this.direction = nearBottom ? "up" : "down";
        }
      }

      if (!itemWithLeastDistance && !this.options.dropOnEmpty)
        //Check if dropOnEmpty is enabled
        return;

      this.currentContainer = this.containers[innermostIndex];
      itemWithLeastDistance
        ? this._rearrange(event, itemWithLeastDistance, null, true)
        : this._rearrange(
            event,
            null,
            this.containers[innermostIndex].element,
            true
          );
      this._trigger("change", event, this._uiHash());
      this.containers[innermostIndex]._trigger(
        "change",
        event,
        this._uiHash(this)
      );

      //Update the placeholder
      this.options.placeholder.update(this.currentContainer, this.placeholder);

      this.containers[innermostIndex]._trigger(
        "over",
        event,
        this._uiHash(this)
      );
      this.containers[innermostIndex].containerCache.over = 1;
    }
  },

  _createHelper: function (event) {
    var o = this.options;
    var helper = $.isFunction(o.helper)
      ? $(o.helper.apply(this.element[0], [event, this.currentItem]))
      : o.helper == "clone"
      ? this.currentItem.clone()
      : this.currentItem;

    if (!helper.parents("body").length)
      //Add the helper to the DOM if that didn't happen already
      $(
        o.appendTo != "parent" ? o.appendTo : this.currentItem[0].parentNode
      )[0].appendChild(helper[0]);

    if (helper[0] == this.currentItem[0])
      this._storedCSS = {
        width: this.currentItem[0].style.width,
        height: this.currentItem[0].style.height,
        position: this.currentItem.css("position"),
        top: this.currentItem.css("top"),
        left: this.currentItem.css("left"),
      };

    if (helper[0].style.width == "" || o.forceHelperSize)
      helper.width(this.currentItem.width());
    if (helper[0].style.height == "" || o.forceHelperSize)
      helper.height(this.currentItem.height());

    return helper;
  },

  _adjustOffsetFromHelper: function (obj) {
    if (typeof obj == "string") {
      obj = obj.split(" ");
    }
    if ($.isArray(obj)) {
      obj = { left: +obj[0], top: +obj[1] || 0 };
    }
    if ("left" in obj) {
      this.offset.click.left = obj.left + this.margins.left;
    }
    if ("right" in obj) {
      this.offset.click.left =
        this.helperProportions.width - obj.right + this.margins.left;
    }
    if ("top" in obj) {
      this.offset.click.top = obj.top + this.margins.top;
    }
    if ("bottom" in obj) {
      this.offset.click.top =
        this.helperProportions.height - obj.bottom + this.margins.top;
    }
  },

  _getParentOffset: function () {
    //Get the offsetParent and cache its position
    this.offsetParent = this.helper.offsetParent();
    var po = this.offsetParent.offset();

    // This is a special case where we need to modify a offset calculated on start, since the following happened:
    // 1. The position of the helper is absolute, so it's position is calculated based on the next positioned parent
    // 2. The actual offset parent is a child of the scroll parent, and the scroll parent isn't the document, which means that
    //    the scroll is included in the initial calculation of the offset of the parent, and never recalculated upon drag
    if (
      this.cssPosition == "absolute" &&
      this.scrollParent[0] != document &&
      $.contains(this.scrollParent[0], this.offsetParent[0])
    ) {
      po.left += this.scrollParent.scrollLeft();
      po.top += this.scrollParent.scrollTop();
    }

    if (
      this.offsetParent[0] == document.body || //This needs to be actually done for all browsers, since pageX/pageY includes this information
      (this.offsetParent[0].tagName &&
        this.offsetParent[0].tagName.toLowerCase() == "html" &&
        $.ui.ie)
    )
      //Ugly IE fix
      po = { top: 0, left: 0 };

    return {
      top:
        po.top + (parseInt(this.offsetParent.css("borderTopWidth"), 10) || 0),
      left:
        po.left + (parseInt(this.offsetParent.css("borderLeftWidth"), 10) || 0),
    };
  },

  _getRelativeOffset: function () {
    if (this.cssPosition == "relative") {
      var p = this.currentItem.position();
      return {
        top:
          p.top -
          (parseInt(this.helper.css("top"), 10) || 0) +
          this.scrollParent.scrollTop(),
        left:
          p.left -
          (parseInt(this.helper.css("left"), 10) || 0) +
          this.scrollParent.scrollLeft(),
      };
    } else {
      return { top: 0, left: 0 };
    }
  },

  _cacheMargins: function () {
    this.margins = {
      left: parseInt(this.currentItem.css("marginLeft"), 10) || 0,
      top: parseInt(this.currentItem.css("marginTop"), 10) || 0,
    };
  },

  _cacheHelperProportions: function () {
    this.helperProportions = {
      width: this.helper.outerWidth(),
      height: this.helper.outerHeight(),
    };
  },

  _setContainment: function () {
    var o = this.options;
    if (o.containment == "parent") o.containment = this.helper[0].parentNode;
    if (o.containment == "document" || o.containment == "window")
      this.containment = [
        0 - this.offset.relative.left - this.offset.parent.left,
        0 - this.offset.relative.top - this.offset.parent.top,
        $(o.containment == "document" ? document : window).width() -
          this.helperProportions.width -
          this.margins.left,
        ($(o.containment == "document" ? document : window).height() ||
          document.body.parentNode.scrollHeight) -
          this.helperProportions.height -
          this.margins.top,
      ];

    if (!/^(document|window|parent)$/.test(o.containment)) {
      var ce = $(o.containment)[0];
      var co = $(o.containment).offset();
      var over = $(ce).css("overflow") != "hidden";

      this.containment = [
        co.left +
          (parseInt($(ce).css("borderLeftWidth"), 10) || 0) +
          (parseInt($(ce).css("paddingLeft"), 10) || 0) -
          this.margins.left,
        co.top +
          (parseInt($(ce).css("borderTopWidth"), 10) || 0) +
          (parseInt($(ce).css("paddingTop"), 10) || 0) -
          this.margins.top,
        co.left +
          (over ? Math.max(ce.scrollWidth, ce.offsetWidth) : ce.offsetWidth) -
          (parseInt($(ce).css("borderLeftWidth"), 10) || 0) -
          (parseInt($(ce).css("paddingRight"), 10) || 0) -
          this.helperProportions.width -
          this.margins.left,
        co.top +
          (over
            ? Math.max(ce.scrollHeight, ce.offsetHeight)
            : ce.offsetHeight) -
          (parseInt($(ce).css("borderTopWidth"), 10) || 0) -
          (parseInt($(ce).css("paddingBottom"), 10) || 0) -
          this.helperProportions.height -
          this.margins.top,
      ];
    }
  },

  _convertPositionTo: function (d, pos) {
    if (!pos) pos = this.position;
    var mod = d == "absolute" ? 1 : -1;
    var o = this.options,
      scroll =
        this.cssPosition == "absolute" &&
        !(
          this.scrollParent[0] != document &&
          $.contains(this.scrollParent[0], this.offsetParent[0])
        )
          ? this.offsetParent
          : this.scrollParent,
      scrollIsRootNode = /(html|body)/i.test(scroll[0].tagName);

    return {
      top:
        pos.top + // The absolute mouse position
        this.offset.relative.top * mod + // Only for relative positioned nodes: Relative offset from element to offset parent
        this.offset.parent.top * mod - // The offsetParent's offset without borders (offset + border)
        (this.cssPosition == "fixed"
          ? -this.scrollParent.scrollTop()
          : scrollIsRootNode
          ? 0
          : scroll.scrollTop()) *
          mod,
      left:
        pos.left + // The absolute mouse position
        this.offset.relative.left * mod + // Only for relative positioned nodes: Relative offset from element to offset parent
        this.offset.parent.left * mod - // The offsetParent's offset without borders (offset + border)
        (this.cssPosition == "fixed"
          ? -this.scrollParent.scrollLeft()
          : scrollIsRootNode
          ? 0
          : scroll.scrollLeft()) *
          mod,
    };
  },

  _generatePosition: function (event) {
    var o = this.options,
      scroll =
        this.cssPosition == "absolute" &&
        !(
          this.scrollParent[0] != document &&
          $.contains(this.scrollParent[0], this.offsetParent[0])
        )
          ? this.offsetParent
          : this.scrollParent,
      scrollIsRootNode = /(html|body)/i.test(scroll[0].tagName);

    // This is another very weird special case that only happens for relative elements:
    // 1. If the css position is relative
    // 2. and the scroll parent is the document or similar to the offset parent
    // we have to refresh the relative offset during the scroll so there are no jumps
    if (
      this.cssPosition == "relative" &&
      !(
        this.scrollParent[0] != document &&
        this.scrollParent[0] != this.offsetParent[0]
      )
    ) {
      this.offset.relative = this._getRelativeOffset();
    }

    var pageX = event.pageX;
    var pageY = event.pageY;

    /*
     * - Position constraining -
     * Constrain the position to a mix of grid, containment.
     */

    if (this.originalPosition) {
      //If we are not dragging yet, we won't check for options

      if (this.containment) {
        if (event.pageX - this.offset.click.left < this.containment[0])
          pageX = this.containment[0] + this.offset.click.left;
        if (event.pageY - this.offset.click.top < this.containment[1])
          pageY = this.containment[1] + this.offset.click.top;
        if (event.pageX - this.offset.click.left > this.containment[2])
          pageX = this.containment[2] + this.offset.click.left;
        if (event.pageY - this.offset.click.top > this.containment[3])
          pageY = this.containment[3] + this.offset.click.top;
      }

      if (o.grid) {
        var top =
          this.originalPageY +
          Math.round((pageY - this.originalPageY) / o.grid[1]) * o.grid[1];
        pageY = this.containment
          ? !(
              top - this.offset.click.top < this.containment[1] ||
              top - this.offset.click.top > this.containment[3]
            )
            ? top
            : !(top - this.offset.click.top < this.containment[1])
            ? top - o.grid[1]
            : top + o.grid[1]
          : top;

        var left =
          this.originalPageX +
          Math.round((pageX - this.originalPageX) / o.grid[0]) * o.grid[0];
        pageX = this.containment
          ? !(
              left - this.offset.click.left < this.containment[0] ||
              left - this.offset.click.left > this.containment[2]
            )
            ? left
            : !(left - this.offset.click.left < this.containment[0])
            ? left - o.grid[0]
            : left + o.grid[0]
          : left;
      }
    }

    return {
      top:
        pageY - // The absolute mouse position
        this.offset.click.top - // Click offset (relative to the element)
        this.offset.relative.top - // Only for relative positioned nodes: Relative offset from element to offset parent
        this.offset.parent.top + // The offsetParent's offset without borders (offset + border)
        (this.cssPosition == "fixed"
          ? -this.scrollParent.scrollTop()
          : scrollIsRootNode
          ? 0
          : scroll.scrollTop()),
      left:
        pageX - // The absolute mouse position
        this.offset.click.left - // Click offset (relative to the element)
        this.offset.relative.left - // Only for relative positioned nodes: Relative offset from element to offset parent
        this.offset.parent.left + // The offsetParent's offset without borders (offset + border)
        (this.cssPosition == "fixed"
          ? -this.scrollParent.scrollLeft()
          : scrollIsRootNode
          ? 0
          : scroll.scrollLeft()),
    };
  },

  _rearrange: function (event, i, a, hardRefresh) {
    a
      ? a[0].appendChild(this.placeholder[0])
      : i.item[0].parentNode.insertBefore(
          this.placeholder[0],
          this.direction == "down" ? i.item[0] : i.item[0].nextSibling
        );

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
  },

  _clear: function (event, noPropagation) {
    this.reverting = false;
    // We delay all events that have to be triggered to after the point where the placeholder has been removed and
    // everything else normalized again
    var delayedTriggers = [];

    // We first have to update the dom position of the actual currentItem
    // Note: don't do it if the current item is already removed (by a user), or it gets reappended (see #4088)
    if (!this._noFinalSort && this.currentItem.parent().length)
      this.placeholder.before(this.currentItem);
    this._noFinalSort = null;

    if (this.helper[0] == this.currentItem[0]) {
      for (var i in this._storedCSS) {
        if (this._storedCSS[i] == "auto" || this._storedCSS[i] == "static")
          this._storedCSS[i] = "";
      }
      this.currentItem.css(this._storedCSS).removeClass("ui-sortable-helper");
    } else {
      this.currentItem.show();
    }

    if (this.fromOutside && !noPropagation)
      delayedTriggers.push(function (event) {
        this._trigger("receive", event, this._uiHash(this.fromOutside));
      });
    if (
      (this.fromOutside ||
        this.domPosition.prev !=
          this.currentItem.prev().not(".ui-sortable-helper")[0] ||
        this.domPosition.parent != this.currentItem.parent()[0]) &&
      !noPropagation
    )
      delayedTriggers.push(function (event) {
        this._trigger("update", event, this._uiHash());
      }); //Trigger update callback if the DOM position has changed

    // Check if the items Container has Changed and trigger appropriate
    // events.
    if (this !== this.currentContainer) {
      if (!noPropagation) {
        delayedTriggers.push(function (event) {
          this._trigger("remove", event, this._uiHash());
        });
        delayedTriggers.push(
          function (c) {
            return function (event) {
              c._trigger("receive", event, this._uiHash(this));
            };
          }.call(this, this.currentContainer)
        );
        delayedTriggers.push(
          function (c) {
            return function (event) {
              c._trigger("update", event, this._uiHash(this));
            };
          }.call(this, this.currentContainer)
        );
      }
    }

    //Post events to containers
    for (var i = this.containers.length - 1; i >= 0; i--) {
      if (!noPropagation)
        delayedTriggers.push(
          function (c) {
            return function (event) {
              c._trigger("deactivate", event, this._uiHash(this));
            };
          }.call(this, this.containers[i])
        );
      if (this.containers[i].containerCache.over) {
        delayedTriggers.push(
          function (c) {
            return function (event) {
              c._trigger("out", event, this._uiHash(this));
            };
          }.call(this, this.containers[i])
        );
        this.containers[i].containerCache.over = 0;
      }
    }

    //Do what was originally in plugins
    if (this._storedCursor) $("body").css("cursor", this._storedCursor); //Reset cursor
    if (this._storedOpacity) this.helper.css("opacity", this._storedOpacity); //Reset opacity
    if (this._storedZIndex)
      this.helper.css(
        "zIndex",
        this._storedZIndex == "auto" ? "" : this._storedZIndex
      ); //Reset z-index

    this.dragging = false;
    if (this.cancelHelperRemoval) {
      if (!noPropagation) {
        this._trigger("beforeStop", event, this._uiHash());
        for (var i = 0; i < delayedTriggers.length; i++) {
          delayedTriggers[i].call(this, event);
        } //Trigger all delayed events
        this._trigger("stop", event, this._uiHash());
      }

      this.fromOutside = false;
      return false;
    }

    if (!noPropagation) this._trigger("beforeStop", event, this._uiHash());

    //$(this.placeholder[0]).remove(); would have been the jQuery way - unfortunately, it unbinds ALL events from the original node!
    this.placeholder[0].parentNode.removeChild(this.placeholder[0]);

    if (this.helper[0] != this.currentItem[0]) this.helper.remove();
    this.helper = null;

    if (!noPropagation) {
      for (var i = 0; i < delayedTriggers.length; i++) {
        delayedTriggers[i].call(this, event);
      } //Trigger all delayed events
      this._trigger("stop", event, this._uiHash());
    }

    this.fromOutside = false;
    return true;
  },

  _trigger: function () {
    if ($.Widget.prototype._trigger.apply(this, arguments) === false) {
      this.cancel();
    }
  },

  _delay: function (handler, delay) {
    function handlerProxy() {
      return (typeof handler === "string" ? instance[handler] : handler).apply(
        instance,
        arguments
      );
    }
    var instance = this;
    return setTimeout(handlerProxy, delay || 0);
  },

  _uiHash: function (_inst) {
    var inst = _inst || this;
    return {
      helper: inst.helper,
      placeholder: inst.placeholder || $([]),
      position: inst.position,
      originalPosition: inst.originalPosition,
      offset: inst.positionAbs,
      item: inst.currentItem,
      sender: _inst ? _inst.element : null,
    };
  },
});
