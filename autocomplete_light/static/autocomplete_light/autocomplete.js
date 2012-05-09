(function($) {
    $(document).bind('yourlabs_autocomplete.activateOption', function(e, autocomplete, option) {
        option.addClass(autocomplete.options.activeClass);
    });
    $(document).bind('yourlabs_autocomplete.deactivateOption', function(e, autocomplete, option) {
        option.removeClass(autocomplete.options.activeClass);
    });

    function Autocomplete(el, options) {
        this.el = el;
        this.el.attr('autocomplete', 'off');
        this.value = '';
        this.xhr = false;
        this.options = {
            url: false,
            timeout: 100,
            id: false,
            minCharacters: 2,
            defaultValue: 'type your search here',
            activeClass: 'active',
			iterablesSelector: 'li:has(a)',
            queryVariable: 'q',
            blurTimeout: 500,
            appendTo: $('body'),
            data: {},
        };
        this.setOptions(options);
        this.initialize();
    }

    $.fn.yourlabs_autocomplete = function(options) {
        var id;
        options = options ? options : {};
        id = options.id || this.attr('id');

        if (!(id && this)) {
            alert('failure: the element needs an id attribute, or an id option must be passed');
            return false;
        }
        
        if ($.fn.yourlabs_autocomplete.registry == undefined) {
            $.fn.yourlabs_autocomplete.registry = {};
        }
        
        if ($.fn.yourlabs_autocomplete.registry[id] == undefined) {
            $.fn.yourlabs_autocomplete.registry[id] = new Autocomplete(this, options);
        }

        return $.fn.yourlabs_autocomplete.registry[id];
    };

    Autocomplete.prototype = {
        initialize: function() {
            var autocomplete;
            autocomplete = this;

            this.el.val(this.options.defaultValue);
            this.el.live('focus', function() {
                if ($(this).val() == autocomplete.options.defaultValue) {
                    $(this).val('');
                }
            });
            this.el.live('blur', function() {
                if ($(this).val() == '') {
                    $(this).val(autocomplete.options.defaultValue);
                }
            });

            $('.yourlabs_autocomplete.inner_container.id_'+this.options.id+' ' + this.options.iterablesSelector).live({
                mouseenter: function(e) {
                    $('.yourlabs_autocomplete.inner_container.id_'+autocomplete.options.id+' ' + autocomplete.options.iterablesSelector + '.' + autocomplete.options.activeClass).each(function() {
                        $(document).trigger('yourlabs_autocomplete.deactivateOption', [autocomplete, $(this)]);
                    });
                    $(document).trigger('yourlabs_autocomplete.activateOption', [autocomplete, $(this)]);
                },
                mouseleave: function(e) {
                    $(document).trigger('yourlabs_autocomplete.deactivateOption', [autocomplete, $(this)]);
                },
                click: function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    autocomplete.el.trigger('yourlabs_autocomplete.selectOption', [$(this)]);
                },
            });

            this.el.keyup(function(e) { autocomplete.refresh(); });

            $('<div id="id_'+this.options.id+'" class="yourlabs_autocomplete outer_container id_'+this.options.id+'" style="position:absolute;z-index:'+this.options.zindex+';"><div class="yourlabs_autocomplete id_'+this.options.id+'"><div class="yourlabs_autocomplete inner_container  id_'+this.options.id+'" style="display:none;"></div></div></div>').appendTo(this.options.appendTo);
            this.innerContainer = $('.yourlabs_autocomplete.inner_container.id_'+this.options.id);
            this.outerContainer = $('.yourlabs_autocomplete.outer_container.id_'+this.options.id);

            if (window.opera) {
                this.el.keypress(function(e) { autocomplete.onKeyPress(e); });
            } else {
                this.el.keydown(function(e) { autocomplete.onKeyPress(e); });
            }
            this.el.blur(function(e) { 
                window.setTimeout(function() {
                    autocomplete.hide(); 
                }, autocomplete.options.blurTimeout);
            });
            //this.el.dblclick(function(e) { autocomplete.show(); });
            this.el.focus(function(e) { autocomplete.show(); });
        },
        onKeyPress: function(e) {
            var option;

            switch (e.keyCode) {
                case 27: //KEY_ESC:
                    this.el.val();
                    this.hide();
                    break;
                case 9: //KEY_TAB:
                    break;
                case 13: //KEY_RETURN:
                    option = this.innerContainer.find(this.options.iterablesSelector + '.' + this.options.activeClass);
                    if (option) {
                        e.preventDefault();
                        e.stopPropagation();
                        this.el.trigger('yourlabs_autocomplete.selectOption', [option]);
                    }
                    if(e.keyCode === 9){ return; }
                    break;
                case 38: //KEY_UP:
                    this.move('up');
                    break;
                case 40: //KEY_DOWN:
                    this.move('down');
                    break;
                default:
                    return;
            }
            e.stopImmediatePropagation();
            e.preventDefault();
        },
        show: function(html) {
            if ($.trim(this.innerContainer.html()).length == 0 && !this.xhr) {
                this.fetchAutocomplete();
                return;
            }
            
            if (html) {
                this.innerContainer.html(html);
            }
            if (!this.innerContainer.is(':visible')) {
                this.outerContainer.show();
                this.innerContainer.show();
            }
        },
        hide: function() {
            this.outerContainer.hide();
            this.innerContainer.hide();
        },
        move: function(way) {
            var current, target, first, last;
            current = this.innerContainer.find(this.options.iterablesSelector + '.' + this.options.activeClass);
            first = this.innerContainer.find(this.options.iterablesSelector + ':first');
            last = this.innerContainer.find(this.options.iterablesSelector + ':last');

            this.show();

            if (current.length) {
                if (way == 'up') {
                    target = current.prevAll(this.options.iterablesSelector + ':first');
                    if (!target.length) {
                        target = last;
                    }
                } else {
                    target = current.nextAll(this.options.iterablesSelector + ':first');
                    if (!target.length) {
                        target = first;
                    }
                }
                $(document).trigger('yourlabs_autocomplete.deactivateOption', [this, current]);
            } else {
                if (way == 'up') {
                    target = last;
                } else {
                    target = first;
                }
            }
            $(document).trigger('yourlabs_autocomplete.activateOption', [this, target]);
        },
        fixPosition: function() {
            var css = {
                'top': Math.floor(this.el.offset()['top']),
                'left': Math.floor(this.el.offset()['left']),
                'position': 'absolute',
            }
            css['top'] += Math.floor(this.el.innerHeight());

            this.outerContainer.css(css);
        },
        refresh: function() {
            var newValue;
            newValue = this.el.val();
            if (newValue == this.options.defaultValue) {
                return false;
            }
            if (newValue.length < this.options.minCharacters) {
                return false;
            }
            if (newValue == this.value) {
                return false;
            }
            this.value = newValue;
            this.fetchAutocomplete();
        },
        fetchAutocomplete: function() {
            var autocomplete, data;

            if (this.xhr) {
                this.xhr.abort();
            }

            autocomplete = this;
            data = this.options.data;
            data[this.options.queryVariable] = this.value;
            this.xhr = $.ajax(this.options.url, {
                'data': data,
                'complete': function(jqXHR, textStatus) {
                    autocomplete.fixPosition();
                    autocomplete.show(jqXHR.responseText);
                },
            });
        },
        setOptions: function(options){
            var o = this.options;
            $.extend(o, options);
        },
    }

}(jQuery));
