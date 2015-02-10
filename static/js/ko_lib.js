//Custom Bindings

ko.bindingHandlers.toggle = {
    init: function (element, valueAccessor) {
        ko.utils.registerEventHandler(element, 'click', function (event) {
            var toggleValue = valueAccessor();
            toggleValue(!toggleValue());
            if (event.preventDefault)
                event.preventDefault();
            event.returnValue = false;
        });
    },
    update: function (element, valueAccessor) {
    }
};

ko.bindingHandlers.disable_content_editable = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
    },
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {
    //console.log(valueAccessor());
        if (valueAccessor()) {
            $(element).text('0.0');
            $(element).removeAttr('contenteditable');
            $(element).attr('disabled','true');
        }
        else {
            $(element).attr('contenteditable', true);
            $(element).attr('required','true');
            $(element).removeAttr('disabled');
        }
    }
}

ko.bindingHandlers.select_all_text = {
    init: function (element, valueAccessor, allBindingsAccessor) {

    },
    update: function (element, valueAccessor, allBindingsAccessor) {
        $(element).on('click', function(){
            $(element).focus();
            $(element).select();
        })
    }
};

ko.bindingHandlers.on_tab = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        $(element).on('keydown', function (event) {
            if (event.keyCode == 9) {

                var fn = valueAccessor();
                fn(element, viewModel);
            }
        });
    },
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {

    }
}

ko.bindingHandlers.enum = {
    init: function (element, valueAccessor) {
        $(element).on('keyup blur', function (event) {
            var va = valueAccessor();
            var input = $(element).text();
            if (jQuery.trim(input)) {
                var values = va['values'];
                var matches = [];
                for (var i = 0; i < values.length; i++) {
                    var search = jQuery.trim(input);
                    var regex = new RegExp(search, "i");
                    if (values[i].match(regex)) {
                        matches.push(values[i]);
                    }
                }
                if (matches.length == 1)
                    $(element).text(matches[0]);
                else
                    $(element).text('');
            }
        });
    },
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {
    }
}

ko.bindingHandlers.textPercent = {
    //init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
    //    //init logic
    //},
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        var val = parseFloat(ko.utils.unwrapObservable(valueAccessor()));
        if ($.isNumeric(val)) {
            $(element).text((val * 100).toFixed(2)) + "%";
        }
        else {
            $(element).text("#Error");
        }
    }
}


ko.bindingHandlers.select2 = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        var value = valueAccessor();
        var allBindings = allBindingsAccessor();

        if (value.constructor == Array) {
            var source = valueAccessor;
            var options = {};
        } else if (allBindings.source) {
            var options = value;
            var source = function () {
                return allBindingsAccessor().source;
            }
        }

        var lookupKey = allBindings.lookupKey || 'id';

//        TODO: test if source()[0] has name but not text
        if (typeof options['formatSelection'] == 'undefined')
            options['formatSelection'] = return_name;
        if (typeof options['formatResult'] == 'undefined')
            options['formatResult'] = return_name;
        if (typeof options['dropdownAutoWidth'] == 'undefined')
            options['dropdownAutoWidth'] = true;
        if (typeof options['initSelection'] == 'undefined')
            options['initSelection'] = init_select2;

        var len = $('.select-drop-klass').length;
        if (typeof options['dropdownCssClass'] == 'undefined')
            options['dropdownCssClass'] = 'select-drop-klass unique-drop' + len;
        $(element).attr('data-counter', len);


        options.query = function (query) {
            var results = [];
            var data = source();
            for (var i in data) {
                if (strip_diacritics('' + data[i].name).toUpperCase().indexOf(strip_diacritics('' + query.term).toUpperCase()) >= 0) {
                    results.push(data[i]);
                }
            }
            query.callback({results: results});
        };

        $(element).select2(options);

        var value = ko.utils.unwrapObservable(allBindings.value);
        $(element).select2('data', ko.utils.arrayFirst(source(), function (item) {
            return item[lookupKey] === value;
        }));

        ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
            $(element).select2('destroy');
        });
    },
    update: function (element, valueAccessor, allBindingsAccessor) {
        var allBindings = allBindingsAccessor(),
            value = ko.utils.unwrapObservable(allBindings.value || allBindings.selectedOptions);

        if (value) {
            $(element).select2('val', value);
        }
    }
};

ko.bindingHandlers.typeahead = {
    init: function (element, valueAccessor) {
        var el = $(element);
        el.attr("autocomplete", "off")
            .typeahead({
                minLength: 0,
                source: function (query, process) {
                    var objects = [];
                    map = {};
                    var data = ko.utils.unwrapObservable(valueAccessor());
                    $.each(data, function (i, object) {
                        map[object.name] = object;
                        objects.push(object.name);
                    });
                    process(objects);
                },
                updater: function (element) {
                    if (map[element]) {
                        $(el).attr('data-selected', map[element].id);
                        return element;
                    } else {
                        return "";
                    }
                }
            });
    }
};

ko.bindingHandlers.flash = {
    init: function (element) {
        $(element).hide().fadeIn('slow');
    }
};

ko.bindingHandlers.eval = {
    init: function (element, valueAccessor) {
    },
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        var value_initial = value;
        if (typeof value == 'undefined')
            return;
        try {
            if (typeof value.indexOf == 'function' && value.indexOf('%') > 0)
                value = calculate_percent(value);
            var val = eval(value);

            if (val != '' && val != null && typeof val != 'undefined'){
            var exponent = Number(val.toExponential().split('e')[1]);
            }

            if(exponent>10 ){
                $(element).addClass('invalid-cell');
                val = value_initial.toString()+' -too large';
                var observable = valueAccessor();
                observable(val);
                $(element).text(val);

            }
            else if(val < 0){
                $(element).addClass('invalid-cell');
                val = value_initial.toString()+' -ve number';
                var observable = valueAccessor();
                observable(val);
                $(element).text(val);
            }


            else{
                // working here console.log(parseFloat(val))
                temp_val =  rnum(parseFloat(val));
                val = znum(temp_val.toString());
                // not working here for 0 console.log(val);
                $(element).text(val);
                var observable = valueAccessor();
                observable(val);
                $(element).removeClass('invalid-cell');
            }

        } catch (e) {
            $(element).addClass('invalid-cell');
            console.log(e);
        }
    }
}


ko.bindingHandlers.eval_for_fuels = {
    init: function (element, valueAccessor) {
    },
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        var value_initial = value;
        if (typeof value == 'undefined')
            return;
        try {
            if (typeof value.indexOf == 'function' && value.indexOf('%') > 0)
                value = calculate_percent(value);
            var val = eval(value);

            if (val != '' && val != null && typeof val != 'undefined'){
            var exponent = Number(val.toExponential().split('e')[1]);
            }

            if(exponent>10 ){
                $(element).addClass('invalid-cell');
                val = value_initial.toString()+' -too large';
                var observable = valueAccessor();
                observable(val);
                $(element).text(val);

            }
            else if(val < 0){
                $(element).addClass('invalid-cell');
                val = value_initial.toString()+' -ve number';
                var observable = valueAccessor();
                observable(val);
                $(element).text(val);
            }


            else{
                // working here console.log(parseFloat(val))
                temp_val =  rnum(parseFloat(val));
                val = znum_for_fuels(temp_val.toString());
                // not working here for 0 console.log(val);
                $(element).text(val);
                var observable = valueAccessor();
                observable(val);
                $(element).removeClass('invalid-cell');
            }

        } catch (e) {
            $(element).addClass('invalid-cell');
            console.log(e);
        }
    }
}


calculate_percent = function (str) {
    str = str.toString();
    str = str.replace(/ /g, '');
    str = str.replace(/([0-9]+)([\+\-\*\/]{1})([0-9]+)%/, function (s, n1, o, n2) {
        var n1 = parseFloat(n1);
        var n2 = parseFloat(n2);
        if (o == '+') {
            return n1 + n1 * n2 / 100;
        }
        if (o == '-') {
            return n1 - n1 * n2 / 100;
        }
        if (o == '*') {
            return n1 * n2 / 100;
        }
        if (o == '/') {
            return 100 * n1 / n2;
        }
        return s;
    });
    return str;
}

ko.bindingHandlers.editableText = {
    init: function (element, valueAccessor) {
        $(element).attr('contenteditable', true);
        $(element).on('blur', function () {
            var observable = valueAccessor();
            if (typeof (observable) == 'function') {
                observable($(this).text());
            }
        });
    },
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        $(element).text(value);
    }
};

ko.bindingHandlers.numeric = {
    init: function (element, valueAccessor) {
        $(element).on('keydown', function (event) {

            // Allow: backspace, delete, tab, escape, and enter
            if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
                // Allow: Ctrl combinations
                (event.ctrlKey === true) ||
                //Allow decimal symbol (.)
                (event.keyCode === 190) ||
                // Allow: home, end, left, right
                (event.keyCode >= 35 && event.keyCode <= 39)) {
                // let it happen, don't do anything
                return;
            }
            else {
                // Ensure that it is a number and stop the keypress
                if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                    event.preventDefault();
                }
            }
        });
    },
    update: function (element, valueAccessor) {
    }
};

//Custom Observable Extensions
ko.extenders.numeric = function (target, precision) {
    //create a writeable computed observable to intercept writes to our observable
    var result = ko.computed({
        read: target,  //always return the original observables value
        write: function (newValue) {
            var current = target(),
                roundingMultiplier = Math.pow(10, precision),
                newValueAsNum = isNaN(newValue) ? current : parseFloat(+newValue),
                valueToWrite = Math.round(newValueAsNum * roundingMultiplier) / roundingMultiplier;

            //only write if it changed
            if (valueToWrite !== current) {
                target(valueToWrite);
            } else {
                //if the rounded value is the same, but a different value was written, force a notification for the current field
                if (newValue !== current) {
                    target.notifySubscribers(valueToWrite);
                }
            }
        }
    });

    //initialize with current value to make sure it is rounded appropriately
    result(target());

    //return the new computed observable
    return result;
};

//Other useful KO-related functions
function setBinding(id, value) {
    var el = document.getElementById(id);
    if (el) {
        el.setAttribute('data-bind', value);
    }
}


// it is the time validator in attendance hour ledger
ko.bindingHandlers.timeValidator = {
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        if(value !== null){
            value = check_time(value);
            if (value == '00:00 PM'){
                value = '12:00 AM';
            }
            $(element).val(value);
            $(element).change();
        }
    }
};


function check_time(value){
    var regex = /(\d{1,2})[:|.](\d{1,2})\s*([am|pm|AM|PM|Am|Pm|aM|pM]*)/gi;
    if(regex.test(value)){
        if(value == '00:00 PM'){
            value = '12:00 AM';
        }
        value.replace(regex, function(_, hour, minute, meridian){
            if (hour > 12 || hour < 1) hour = 12;
            if (minute < 1 ||  minute > 59) minute = 0;


            hour = make_2_digit(hour);
            minute = make_2_digit(minute);
            if(meridian == '' || meridian.indexOf('p') >= 0 || meridian.indexOf('P') >= 0){
                meridian = 'PM';
            }
            else{
                meridian = 'AM';
            }
            value = hour + ':' + minute + ' ' + meridian;
        });
    }
    else{
        if(value){
            value = '12:00 PM';
        }
    }
    return value;
}


function make_2_digit(num){
    var s_num = num.toString()
    if (s_num.length == 1)
        return '0' + s_num;
    else
        return num.toString();
}
