ko.bindingHandlers.toggle={init:function(element,valueAccessor){ko.utils.registerEventHandler(element,'click',function(event){var toggleValue=valueAccessor();toggleValue(!toggleValue());if(event.preventDefault)
event.preventDefault();event.returnValue=false;});},update:function(element,valueAccessor){}};ko.bindingHandlers.disable_content_editable={init:function(element,valueAccessor,allBindingsAccessor,viewModel){},update:function(element,valueAccessor,allBindingsAccessor,viewModel){if(valueAccessor()){$(element).text('0.0');$(element).removeAttr('contenteditable');$(element).attr('disabled','true');}
else{$(element).attr('contenteditable',true);$(element).attr('required','true');$(element).removeAttr('disabled');}}}
ko.bindingHandlers.select_all_text={init:function(element,valueAccessor,allBindingsAccessor){},update:function(element,valueAccessor,allBindingsAccessor){$(element).on('click',function(){$(element).focus();$(element).select();})}};ko.bindingHandlers.on_tab={init:function(element,valueAccessor,allBindingsAccessor,viewModel){$(element).on('keydown',function(event){if(event.keyCode==9){var fn=valueAccessor();fn(element,viewModel);}});},update:function(element,valueAccessor,allBindingsAccessor,viewModel){}}
ko.bindingHandlers.enum={init:function(element,valueAccessor){$(element).on('keyup blur',function(event){var va=valueAccessor();var input=$(element).text();if(jQuery.trim(input)){var values=va['values'];var matches=[];for(var i=0;i<values.length;i++){var search=jQuery.trim(input);var regex=new RegExp(search,"i");if(values[i].match(regex)){matches.push(values[i]);}}
if(matches.length==1)
$(element).text(matches[0]);else
$(element).text('');}});},update:function(element,valueAccessor,allBindingsAccessor,viewModel){}}
ko.bindingHandlers.textPercent={update:function(element,valueAccessor,allBindingsAccessor,viewModel){var val=parseFloat(ko.utils.unwrapObservable(valueAccessor()));if($.isNumeric(val)){$(element).text((val*100).toFixed(2))+"%";}
else{$(element).text("#Error");}}}
ko.bindingHandlers.select2={init:function(element,valueAccessor,allBindingsAccessor){var value=valueAccessor();var allBindings=allBindingsAccessor();if(value.constructor==Array){var source=valueAccessor;var options={};}else if(allBindings.source){var options=value;var source=function(){return allBindingsAccessor().source;}}
var lookupKey=allBindings.lookupKey||'id';if(typeof options['formatSelection']=='undefined')
options['formatSelection']=return_name;if(typeof options['formatResult']=='undefined')
options['formatResult']=return_name;if(typeof options['dropdownAutoWidth']=='undefined')
options['dropdownAutoWidth']=true;if(typeof options['initSelection']=='undefined')
options['initSelection']=init_select2;var len=$('.select-drop-klass').length;if(typeof options['dropdownCssClass']=='undefined')
options['dropdownCssClass']='select-drop-klass unique-drop'+len;$(element).attr('data-counter',len);options.query=function(query){var results=[];var data=source();for(var i in data){if(strip_diacritics(''+data[i].name).toUpperCase().indexOf(strip_diacritics(''+query.term).toUpperCase())>=0){results.push(data[i]);}}
query.callback({results:results});};$(element).select2(options);var value=ko.utils.unwrapObservable(allBindings.value);$(element).select2('data',ko.utils.arrayFirst(source(),function(item){return item[lookupKey]===value;}));ko.utils.domNodeDisposal.addDisposeCallback(element,function(){$(element).select2('destroy');});},update:function(element,valueAccessor,allBindingsAccessor){var allBindings=allBindingsAccessor(),value=ko.utils.unwrapObservable(allBindings.value||allBindings.selectedOptions);if(value){$(element).select2('val',value);}}};ko.bindingHandlers.typeahead={init:function(element,valueAccessor){var el=$(element);el.attr("autocomplete","off").typeahead({minLength:0,source:function(query,process){var objects=[];map={};var data=ko.utils.unwrapObservable(valueAccessor());$.each(data,function(i,object){map[object.name]=object;objects.push(object.name);});process(objects);},updater:function(element){if(map[element]){$(el).attr('data-selected',map[element].id);return element;}else{return"";}}});}};ko.bindingHandlers.flash={init:function(element){$(element).hide().fadeIn('slow');}};ko.bindingHandlers.eval={init:function(element,valueAccessor){},update:function(element,valueAccessor){var value=ko.utils.unwrapObservable(valueAccessor());var value_initial=value;if(typeof value=='undefined')
return;try{if(typeof value.indexOf=='function'&&value.indexOf('%')>0)
value=calculate_percent(value);var val=eval(value);if(val!=''&&val!=null&&typeof val!='undefined'){var exponent=Number(val.toExponential().split('e')[1]);}
if(exponent>10){$(element).addClass('invalid-cell');val=value_initial.toString()+' -too large';var observable=valueAccessor();observable(val);$(element).text(val);}
else if(val<0){$(element).addClass('invalid-cell');val=value_initial.toString()+' -ve number';var observable=valueAccessor();observable(val);$(element).text(val);}
else{temp_val=rnum(parseFloat(val));val=znum(temp_val.toString());$(element).text(val);var observable=valueAccessor();observable(val);$(element).removeClass('invalid-cell');}}catch(e){$(element).addClass('invalid-cell');console.log(e);}}}
ko.bindingHandlers.eval_for_fuels={init:function(element,valueAccessor){},update:function(element,valueAccessor){var value=ko.utils.unwrapObservable(valueAccessor());var value_initial=value;if(typeof value=='undefined')
return;try{if(typeof value.indexOf=='function'&&value.indexOf('%')>0)
value=calculate_percent(value);var val=eval(value);if(val!=''&&val!=null&&typeof val!='undefined'){var exponent=Number(val.toExponential().split('e')[1]);}
if(exponent>10){$(element).addClass('invalid-cell');val=value_initial.toString()+' -too large';var observable=valueAccessor();observable(val);$(element).text(val);}
else if(val<0){$(element).addClass('invalid-cell');val=value_initial.toString()+' -ve number';var observable=valueAccessor();observable(val);$(element).text(val);}
else{temp_val=rnum(parseFloat(val));val=znum_for_fuels(temp_val.toString());$(element).text(val);var observable=valueAccessor();observable(val);$(element).removeClass('invalid-cell');}}catch(e){$(element).addClass('invalid-cell');console.log(e);}}}
calculate_percent=function(str){str=str.toString();str=str.replace(/ /g,'');str=str.replace(/([0-9]+)([\+\-\*\/]{1})([0-9]+)%/,function(s,n1,o,n2){var n1=parseFloat(n1);var n2=parseFloat(n2);if(o=='+'){return n1+n1*n2/100;}
if(o=='-'){return n1-n1*n2/100;}
if(o=='*'){return n1*n2/100;}
if(o=='/'){return 100*n1/n2;}
return s;});return str;}
ko.bindingHandlers.editableText={init:function(element,valueAccessor){$(element).attr('contenteditable',true);$(element).on('blur',function(){var observable=valueAccessor();if(typeof(observable)=='function'){observable($(this).text());}});},update:function(element,valueAccessor){var value=ko.utils.unwrapObservable(valueAccessor());$(element).text(value);}};ko.bindingHandlers.numeric={init:function(element,valueAccessor){$(element).on('keydown',function(event){if(event.keyCode==46||event.keyCode==8||event.keyCode==9||event.keyCode==27||event.keyCode==13||(event.ctrlKey===true)||(event.keyCode===190)||(event.keyCode>=35&&event.keyCode<=39)){return;}
else{if(event.shiftKey||(event.keyCode<48||event.keyCode>57)&&(event.keyCode<96||event.keyCode>105)){event.preventDefault();}}});},update:function(element,valueAccessor){}};ko.extenders.numeric=function(target,precision){var result=ko.computed({read:target,write:function(newValue){var current=target(),roundingMultiplier=Math.pow(10,precision),newValueAsNum=isNaN(newValue)?current:parseFloat(+newValue),valueToWrite=Math.round(newValueAsNum*roundingMultiplier)/roundingMultiplier;if(valueToWrite!==current){target(valueToWrite);}else{if(newValue!==current){target.notifySubscribers(valueToWrite);}}}});result(target());return result;};function setBinding(id,value){var el=document.getElementById(id);if(el){el.setAttribute('data-bind',value);}}
ko.bindingHandlers.timeValidator={update:function(element,valueAccessor){var value=ko.utils.unwrapObservable(valueAccessor());if(value!==null){value=check_time(value);if(value=='00:00 PM'){value='12:00 AM';}
$(element).val(value);$(element).change();}}};function check_time(value){var regex=/(\d{1,2})[:|.](\d{1,2})\s*([am|pm|AM|PM|Am|Pm|aM|pM]*)/gi;if(regex.test(value)){if(value=='00:00 PM'){value='12:00 AM';}
value.replace(regex,function(_,hour,minute,meridian){if(hour>12||hour<1)hour=12;if(minute<1||minute>59)minute=0;hour=make_2_digit(hour);minute=make_2_digit(minute);if(meridian==''||meridian.indexOf('p')>=0||meridian.indexOf('P')>=0){meridian='PM';}
else{meridian='AM';}
value=hour+':'+minute+' '+meridian;});}
else{if(value){value='12:00 PM';}}
return value;}
function make_2_digit(num){var s_num=num.toString()
if(s_num.length==1)
return'0'+s_num;else
return num.toString();}
function init_select2(element,callback){if($(element).data('url')){if($(element).data('name')){var name=$(element).data('name');}else{var matches=$(element).data('bind').match(/value: ([a-z_1-9]+)/);if(matches){var name=matches[1].replace(/_id/,'').replace(/_/g,' ').toTitleCase();}else{var name='Object';}}
var drop_el=$('.unique-drop'+$(element).data('counter'));if(!$('#appended-link'+$(element).data('counter')).length){var appended_link=jQuery('<a/>',{id:'appended-link'+$(element).data('counter'),class:'appended-link',href:$(element).data('url'),title:'Add New '+name,text:'Add New '+name,'data-toggle':'modal'});appended_link.appendTo(drop_el).on('click',[$(element)],appended_link_clicked);}
else{var appended_link=jQuery('<a/>',{id:'appended-link'+$(element).data('counter'),class:'appended-link',href:$(element).data('url'),title:'Add New '+name,text:'Add New '+name,'data-toggle':'modal'});appended_link.appendTo(drop_el).on('click',[$(element)],appended_link_clicked);}
var temp="a[id='appended-link"+$(element).data('counter')+"']";$(temp).not(":last").remove();}}
appended_link_clicked=function(e){get_target(e).parent().toggle();if(!window.last_active_select){window.last_active_select=new Array();}
window.last_active_select.push(e.data[0]);e.preventDefault();var the_modal=bs_modal.create();var url=$(this).attr('href');if(url.indexOf('#')==0){$(url).modal('open');}else{var old_forms=$('form');$.get(url,function(data){the_modal.html(data).modal();}).success(function(){var new_forms=$('form').not(old_forms).get();$(new_forms).submit({url:url},override_form);the_modal.on('shown',function(){$('input:text:visible:first',this).focus();});$(new_forms).each(function(form){apply_select2(new_forms[form]);});});}
return false;}
function return_name(obj){return obj.name;}
DIACRITICS={"\u24B6":"A","\uFF21":"A","\u00C0":"A","\u00C1":"A","\u00C2":"A","\u1EA6":"A","\u1EA4":"A","\u1EAA":"A","\u1EA8":"A","\u00C3":"A","\u0100":"A","\u0102":"A","\u1EB0":"A","\u1EAE":"A","\u1EB4":"A","\u1EB2":"A","\u0226":"A","\u01E0":"A","\u00C4":"A","\u01DE":"A","\u1EA2":"A","\u00C5":"A","\u01FA":"A","\u01CD":"A","\u0200":"A","\u0202":"A","\u1EA0":"A","\u1EAC":"A","\u1EB6":"A","\u1E00":"A","\u0104":"A","\u023A":"A","\u2C6F":"A","\uA732":"AA","\u00C6":"AE","\u01FC":"AE","\u01E2":"AE","\uA734":"AO","\uA736":"AU","\uA738":"AV","\uA73A":"AV","\uA73C":"AY","\u24B7":"B","\uFF22":"B","\u1E02":"B","\u1E04":"B","\u1E06":"B","\u0243":"B","\u0182":"B","\u0181":"B","\u24B8":"C","\uFF23":"C","\u0106":"C","\u0108":"C","\u010A":"C","\u010C":"C","\u00C7":"C","\u1E08":"C","\u0187":"C","\u023B":"C","\uA73E":"C","\u24B9":"D","\uFF24":"D","\u1E0A":"D","\u010E":"D","\u1E0C":"D","\u1E10":"D","\u1E12":"D","\u1E0E":"D","\u0110":"D","\u018B":"D","\u018A":"D","\u0189":"D","\uA779":"D","\u01F1":"DZ","\u01C4":"DZ","\u01F2":"Dz","\u01C5":"Dz","\u24BA":"E","\uFF25":"E","\u00C8":"E","\u00C9":"E","\u00CA":"E","\u1EC0":"E","\u1EBE":"E","\u1EC4":"E","\u1EC2":"E","\u1EBC":"E","\u0112":"E","\u1E14":"E","\u1E16":"E","\u0114":"E","\u0116":"E","\u00CB":"E","\u1EBA":"E","\u011A":"E","\u0204":"E","\u0206":"E","\u1EB8":"E","\u1EC6":"E","\u0228":"E","\u1E1C":"E","\u0118":"E","\u1E18":"E","\u1E1A":"E","\u0190":"E","\u018E":"E","\u24BB":"F","\uFF26":"F","\u1E1E":"F","\u0191":"F","\uA77B":"F","\u24BC":"G","\uFF27":"G","\u01F4":"G","\u011C":"G","\u1E20":"G","\u011E":"G","\u0120":"G","\u01E6":"G","\u0122":"G","\u01E4":"G","\u0193":"G","\uA7A0":"G","\uA77D":"G","\uA77E":"G","\u24BD":"H","\uFF28":"H","\u0124":"H","\u1E22":"H","\u1E26":"H","\u021E":"H","\u1E24":"H","\u1E28":"H","\u1E2A":"H","\u0126":"H","\u2C67":"H","\u2C75":"H","\uA78D":"H","\u24BE":"I","\uFF29":"I","\u00CC":"I","\u00CD":"I","\u00CE":"I","\u0128":"I","\u012A":"I","\u012C":"I","\u0130":"I","\u00CF":"I","\u1E2E":"I","\u1EC8":"I","\u01CF":"I","\u0208":"I","\u020A":"I","\u1ECA":"I","\u012E":"I","\u1E2C":"I","\u0197":"I","\u24BF":"J","\uFF2A":"J","\u0134":"J","\u0248":"J","\u24C0":"K","\uFF2B":"K","\u1E30":"K","\u01E8":"K","\u1E32":"K","\u0136":"K","\u1E34":"K","\u0198":"K","\u2C69":"K","\uA740":"K","\uA742":"K","\uA744":"K","\uA7A2":"K","\u24C1":"L","\uFF2C":"L","\u013F":"L","\u0139":"L","\u013D":"L","\u1E36":"L","\u1E38":"L","\u013B":"L","\u1E3C":"L","\u1E3A":"L","\u0141":"L","\u023D":"L","\u2C62":"L","\u2C60":"L","\uA748":"L","\uA746":"L","\uA780":"L","\u01C7":"LJ","\u01C8":"Lj","\u24C2":"M","\uFF2D":"M","\u1E3E":"M","\u1E40":"M","\u1E42":"M","\u2C6E":"M","\u019C":"M","\u24C3":"N","\uFF2E":"N","\u01F8":"N","\u0143":"N","\u00D1":"N","\u1E44":"N","\u0147":"N","\u1E46":"N","\u0145":"N","\u1E4A":"N","\u1E48":"N","\u0220":"N","\u019D":"N","\uA790":"N","\uA7A4":"N","\u01CA":"NJ","\u01CB":"Nj","\u24C4":"O","\uFF2F":"O","\u00D2":"O","\u00D3":"O","\u00D4":"O","\u1ED2":"O","\u1ED0":"O","\u1ED6":"O","\u1ED4":"O","\u00D5":"O","\u1E4C":"O","\u022C":"O","\u1E4E":"O","\u014C":"O","\u1E50":"O","\u1E52":"O","\u014E":"O","\u022E":"O","\u0230":"O","\u00D6":"O","\u022A":"O","\u1ECE":"O","\u0150":"O","\u01D1":"O","\u020C":"O","\u020E":"O","\u01A0":"O","\u1EDC":"O","\u1EDA":"O","\u1EE0":"O","\u1EDE":"O","\u1EE2":"O","\u1ECC":"O","\u1ED8":"O","\u01EA":"O","\u01EC":"O","\u00D8":"O","\u01FE":"O","\u0186":"O","\u019F":"O","\uA74A":"O","\uA74C":"O","\u01A2":"OI","\uA74E":"OO","\u0222":"OU","\u24C5":"P","\uFF30":"P","\u1E54":"P","\u1E56":"P","\u01A4":"P","\u2C63":"P","\uA750":"P","\uA752":"P","\uA754":"P","\u24C6":"Q","\uFF31":"Q","\uA756":"Q","\uA758":"Q","\u024A":"Q","\u24C7":"R","\uFF32":"R","\u0154":"R","\u1E58":"R","\u0158":"R","\u0210":"R","\u0212":"R","\u1E5A":"R","\u1E5C":"R","\u0156":"R","\u1E5E":"R","\u024C":"R","\u2C64":"R","\uA75A":"R","\uA7A6":"R","\uA782":"R","\u24C8":"S","\uFF33":"S","\u1E9E":"S","\u015A":"S","\u1E64":"S","\u015C":"S","\u1E60":"S","\u0160":"S","\u1E66":"S","\u1E62":"S","\u1E68":"S","\u0218":"S","\u015E":"S","\u2C7E":"S","\uA7A8":"S","\uA784":"S","\u24C9":"T","\uFF34":"T","\u1E6A":"T","\u0164":"T","\u1E6C":"T","\u021A":"T","\u0162":"T","\u1E70":"T","\u1E6E":"T","\u0166":"T","\u01AC":"T","\u01AE":"T","\u023E":"T","\uA786":"T","\uA728":"TZ","\u24CA":"U","\uFF35":"U","\u00D9":"U","\u00DA":"U","\u00DB":"U","\u0168":"U","\u1E78":"U","\u016A":"U","\u1E7A":"U","\u016C":"U","\u00DC":"U","\u01DB":"U","\u01D7":"U","\u01D5":"U","\u01D9":"U","\u1EE6":"U","\u016E":"U","\u0170":"U","\u01D3":"U","\u0214":"U","\u0216":"U","\u01AF":"U","\u1EEA":"U","\u1EE8":"U","\u1EEE":"U","\u1EEC":"U","\u1EF0":"U","\u1EE4":"U","\u1E72":"U","\u0172":"U","\u1E76":"U","\u1E74":"U","\u0244":"U","\u24CB":"V","\uFF36":"V","\u1E7C":"V","\u1E7E":"V","\u01B2":"V","\uA75E":"V","\u0245":"V","\uA760":"VY","\u24CC":"W","\uFF37":"W","\u1E80":"W","\u1E82":"W","\u0174":"W","\u1E86":"W","\u1E84":"W","\u1E88":"W","\u2C72":"W","\u24CD":"X","\uFF38":"X","\u1E8A":"X","\u1E8C":"X","\u24CE":"Y","\uFF39":"Y","\u1EF2":"Y","\u00DD":"Y","\u0176":"Y","\u1EF8":"Y","\u0232":"Y","\u1E8E":"Y","\u0178":"Y","\u1EF6":"Y","\u1EF4":"Y","\u01B3":"Y","\u024E":"Y","\u1EFE":"Y","\u24CF":"Z","\uFF3A":"Z","\u0179":"Z","\u1E90":"Z","\u017B":"Z","\u017D":"Z","\u1E92":"Z","\u1E94":"Z","\u01B5":"Z","\u0224":"Z","\u2C7F":"Z","\u2C6B":"Z","\uA762":"Z","\u24D0":"a","\uFF41":"a","\u1E9A":"a","\u00E0":"a","\u00E1":"a","\u00E2":"a","\u1EA7":"a","\u1EA5":"a","\u1EAB":"a","\u1EA9":"a","\u00E3":"a","\u0101":"a","\u0103":"a","\u1EB1":"a","\u1EAF":"a","\u1EB5":"a","\u1EB3":"a","\u0227":"a","\u01E1":"a","\u00E4":"a","\u01DF":"a","\u1EA3":"a","\u00E5":"a","\u01FB":"a","\u01CE":"a","\u0201":"a","\u0203":"a","\u1EA1":"a","\u1EAD":"a","\u1EB7":"a","\u1E01":"a","\u0105":"a","\u2C65":"a","\u0250":"a","\uA733":"aa","\u00E6":"ae","\u01FD":"ae","\u01E3":"ae","\uA735":"ao","\uA737":"au","\uA739":"av","\uA73B":"av","\uA73D":"ay","\u24D1":"b","\uFF42":"b","\u1E03":"b","\u1E05":"b","\u1E07":"b","\u0180":"b","\u0183":"b","\u0253":"b","\u24D2":"c","\uFF43":"c","\u0107":"c","\u0109":"c","\u010B":"c","\u010D":"c","\u00E7":"c","\u1E09":"c","\u0188":"c","\u023C":"c","\uA73F":"c","\u2184":"c","\u24D3":"d","\uFF44":"d","\u1E0B":"d","\u010F":"d","\u1E0D":"d","\u1E11":"d","\u1E13":"d","\u1E0F":"d","\u0111":"d","\u018C":"d","\u0256":"d","\u0257":"d","\uA77A":"d","\u01F3":"dz","\u01C6":"dz","\u24D4":"e","\uFF45":"e","\u00E8":"e","\u00E9":"e","\u00EA":"e","\u1EC1":"e","\u1EBF":"e","\u1EC5":"e","\u1EC3":"e","\u1EBD":"e","\u0113":"e","\u1E15":"e","\u1E17":"e","\u0115":"e","\u0117":"e","\u00EB":"e","\u1EBB":"e","\u011B":"e","\u0205":"e","\u0207":"e","\u1EB9":"e","\u1EC7":"e","\u0229":"e","\u1E1D":"e","\u0119":"e","\u1E19":"e","\u1E1B":"e","\u0247":"e","\u025B":"e","\u01DD":"e","\u24D5":"f","\uFF46":"f","\u1E1F":"f","\u0192":"f","\uA77C":"f","\u24D6":"g","\uFF47":"g","\u01F5":"g","\u011D":"g","\u1E21":"g","\u011F":"g","\u0121":"g","\u01E7":"g","\u0123":"g","\u01E5":"g","\u0260":"g","\uA7A1":"g","\u1D79":"g","\uA77F":"g","\u24D7":"h","\uFF48":"h","\u0125":"h","\u1E23":"h","\u1E27":"h","\u021F":"h","\u1E25":"h","\u1E29":"h","\u1E2B":"h","\u1E96":"h","\u0127":"h","\u2C68":"h","\u2C76":"h","\u0265":"h","\u0195":"hv","\u24D8":"i","\uFF49":"i","\u00EC":"i","\u00ED":"i","\u00EE":"i","\u0129":"i","\u012B":"i","\u012D":"i","\u00EF":"i","\u1E2F":"i","\u1EC9":"i","\u01D0":"i","\u0209":"i","\u020B":"i","\u1ECB":"i","\u012F":"i","\u1E2D":"i","\u0268":"i","\u0131":"i","\u24D9":"j","\uFF4A":"j","\u0135":"j","\u01F0":"j","\u0249":"j","\u24DA":"k","\uFF4B":"k","\u1E31":"k","\u01E9":"k","\u1E33":"k","\u0137":"k","\u1E35":"k","\u0199":"k","\u2C6A":"k","\uA741":"k","\uA743":"k","\uA745":"k","\uA7A3":"k","\u24DB":"l","\uFF4C":"l","\u0140":"l","\u013A":"l","\u013E":"l","\u1E37":"l","\u1E39":"l","\u013C":"l","\u1E3D":"l","\u1E3B":"l","\u017F":"l","\u0142":"l","\u019A":"l","\u026B":"l","\u2C61":"l","\uA749":"l","\uA781":"l","\uA747":"l","\u01C9":"lj","\u24DC":"m","\uFF4D":"m","\u1E3F":"m","\u1E41":"m","\u1E43":"m","\u0271":"m","\u026F":"m","\u24DD":"n","\uFF4E":"n","\u01F9":"n","\u0144":"n","\u00F1":"n","\u1E45":"n","\u0148":"n","\u1E47":"n","\u0146":"n","\u1E4B":"n","\u1E49":"n","\u019E":"n","\u0272":"n","\u0149":"n","\uA791":"n","\uA7A5":"n","\u01CC":"nj","\u24DE":"o","\uFF4F":"o","\u00F2":"o","\u00F3":"o","\u00F4":"o","\u1ED3":"o","\u1ED1":"o","\u1ED7":"o","\u1ED5":"o","\u00F5":"o","\u1E4D":"o","\u022D":"o","\u1E4F":"o","\u014D":"o","\u1E51":"o","\u1E53":"o","\u014F":"o","\u022F":"o","\u0231":"o","\u00F6":"o","\u022B":"o","\u1ECF":"o","\u0151":"o","\u01D2":"o","\u020D":"o","\u020F":"o","\u01A1":"o","\u1EDD":"o","\u1EDB":"o","\u1EE1":"o","\u1EDF":"o","\u1EE3":"o","\u1ECD":"o","\u1ED9":"o","\u01EB":"o","\u01ED":"o","\u00F8":"o","\u01FF":"o","\u0254":"o","\uA74B":"o","\uA74D":"o","\u0275":"o","\u01A3":"oi","\u0223":"ou","\uA74F":"oo","\u24DF":"p","\uFF50":"p","\u1E55":"p","\u1E57":"p","\u01A5":"p","\u1D7D":"p","\uA751":"p","\uA753":"p","\uA755":"p","\u24E0":"q","\uFF51":"q","\u024B":"q","\uA757":"q","\uA759":"q","\u24E1":"r","\uFF52":"r","\u0155":"r","\u1E59":"r","\u0159":"r","\u0211":"r","\u0213":"r","\u1E5B":"r","\u1E5D":"r","\u0157":"r","\u1E5F":"r","\u024D":"r","\u027D":"r","\uA75B":"r","\uA7A7":"r","\uA783":"r","\u24E2":"s","\uFF53":"s","\u00DF":"s","\u015B":"s","\u1E65":"s","\u015D":"s","\u1E61":"s","\u0161":"s","\u1E67":"s","\u1E63":"s","\u1E69":"s","\u0219":"s","\u015F":"s","\u023F":"s","\uA7A9":"s","\uA785":"s","\u1E9B":"s","\u24E3":"t","\uFF54":"t","\u1E6B":"t","\u1E97":"t","\u0165":"t","\u1E6D":"t","\u021B":"t","\u0163":"t","\u1E71":"t","\u1E6F":"t","\u0167":"t","\u01AD":"t","\u0288":"t","\u2C66":"t","\uA787":"t","\uA729":"tz","\u24E4":"u","\uFF55":"u","\u00F9":"u","\u00FA":"u","\u00FB":"u","\u0169":"u","\u1E79":"u","\u016B":"u","\u1E7B":"u","\u016D":"u","\u00FC":"u","\u01DC":"u","\u01D8":"u","\u01D6":"u","\u01DA":"u","\u1EE7":"u","\u016F":"u","\u0171":"u","\u01D4":"u","\u0215":"u","\u0217":"u","\u01B0":"u","\u1EEB":"u","\u1EE9":"u","\u1EEF":"u","\u1EED":"u","\u1EF1":"u","\u1EE5":"u","\u1E73":"u","\u0173":"u","\u1E77":"u","\u1E75":"u","\u0289":"u","\u24E5":"v","\uFF56":"v","\u1E7D":"v","\u1E7F":"v","\u028B":"v","\uA75F":"v","\u028C":"v","\uA761":"vy","\u24E6":"w","\uFF57":"w","\u1E81":"w","\u1E83":"w","\u0175":"w","\u1E87":"w","\u1E85":"w","\u1E98":"w","\u1E89":"w","\u2C73":"w","\u24E7":"x","\uFF58":"x","\u1E8B":"x","\u1E8D":"x","\u24E8":"y","\uFF59":"y","\u1EF3":"y","\u00FD":"y","\u0177":"y","\u1EF9":"y","\u0233":"y","\u1E8F":"y","\u00FF":"y","\u1EF7":"y","\u1E99":"y","\u1EF5":"y","\u01B4":"y","\u024F":"y","\u1EFF":"y","\u24E9":"z","\uFF5A":"z","\u017A":"z","\u1E91":"z","\u017C":"z","\u017E":"z","\u1E93":"z","\u1E95":"z","\u01B6":"z","\u0225":"z","\u0240":"z","\u2C6C":"z","\uA763":"z"};function strip_diacritics(str){var ret,i,l,c;if(!str||str.length<1)return str;ret="";for(i=0,l=str.length;i<l;i++){c=str.charAt(i);ret+=DIACRITICS[c]||c;}
return ret;}
$(document).ready(function(){apply_select2();$('.btn-danger').click(function(e){if(confirm('Are you sure you want to delete?')){return true;}else return false;});$('.change-on-ready').trigger('change');$('.col-box a').click(function(e){e.preventDefault();$(this).parent('.col-box-header').siblings('.col-box-body').slideToggle();$(this).find('.status-handle').toggleClass('icon-chevron-down');});});apply_select2=function(form){if(typeof form!='undefined'){var selection=$(form).find('.select2')}
else{var selection=$('.select2');}
selection.each(function(){var element=this;var len=$('.select-drop-klass').length;var drop_class='select-drop-klass unique-drop'+len;$(element).attr('data-counter',len);var options_dict={'dropdownCssClass':drop_class,'dropdownAutoWidth':true,'width':'resolve'}
if($(element).hasClass('placehold'))
options_dict['placeholderOption']='first';$(element).select2(options_dict);if($(element).data('url')){if(!$('#appended-link'+$(element).data('counter')).length){if($(element).data('name'))
var field_name=$(element).data('name');else
var field_name=$(element).attr('name').replace(/_/g,' ').toTitleCase();jQuery('<a/>',{class:'appended-link',id:'appended-link'+$(element).data('counter'),href:$(element).data('url'),title:'Add New '+field_name,text:'Add New '+field_name,'data-toggle':'modal'}).appendTo($('.unique-drop'+len)).on('click',[element],appended_link_clicked);}}});}
override_form=function(event){var $form=$(this);var $target=$('#modal'+$('.modal').length);var action=$form.attr('action');if(typeof action=='undefined'){action=event.data.url;}
$.ajax({type:$form.attr('method'),url:action,data:$form.serialize(),success:function(data,status){$target.html(data);$target.find('form').submit({url:action},override_form);}});event.preventDefault();}
on_form_submit=function(event){var $form=$(this);var $target=$($form.attr('data-target'));$.ajax({type:$form.attr('method'),url:$form.attr('action'),data:$form.serialize(),success:function(data,status){$target.html(data);}});event.preventDefault();}
function compare_arrays(arr1,arr2){return $(arr1).not(arr2).length==0&&$(arr2).not(arr1).length==0;}
function intersect_safe(a,b){var ai=0,bi=0;var result=new Array();while(ai<a.length&&bi<b.length){if(a[ai]<b[bi]){ai++;}
else if(a[ai]>b[bi]){bi++;}
else
{result.push(a[ai]);ai++;bi++;}}
return result;}
function intersection(arr1,arr2){var temp=[];for(var i in arr1){var element=arr1[i];if(arr2.indexOf(element)>-1){temp.push(element);}}
return temp;}
function rnum(n){if(!isAN(n))
return'';var b=Math.round(n*Math.pow(10,global_settings.decimal_places))/Math.pow(10,global_settings.decimal_places);var a=b.toString();var reg="/^(?:\d*\.\d{1,"+global_settings.decimal_places.toString()+"}|\d+)$/";a.match(reg);return parseFloat(a);}
function znum(n){if(typeof n=='undefined'||n==null)
return'';else if(n==''||n=='0'){return''}
else
{var s=n
if(s.indexOf('.')==-1)s+='.';while(s.length<s.indexOf('.')+global_settings.decimal_places+1)s+='0';return s;}}
function znum_for_fuels(n){if(typeof n=='undefined'||n==null)
return'';else if(n==''){return''}
else
{var s=n
if(s.indexOf('.')==-1)s+='.';while(s.length<s.indexOf('.')+global_settings.decimal_places+1)s+='0';return s;}}
function fnum(n){if(typeof n=='undefined')
return'';if(global_settings.number_comma_system=='no')
return n;else if(global_settings.number_comma_system=='120,000')
return comma_in_thou(n);else
return comma_in_indian(n);}
function comma_in_thou(x){return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g,",");}
function comma_in_indian(x){x=x.toString();var afterPoint='';if(x.indexOf('.')>0)
afterPoint=x.substring(x.indexOf('.'),x.length);x=Math.floor(x);x=x.toString();var lastThree=x.substring(x.length-3);var otherNumbers=x.substring(0,x.length-3);if(otherNumbers!='')
lastThree=','+lastThree;var res=otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g,",")+lastThree+afterPoint;return res;}
function strip_commas(n){if(n==''||n==null)
return 0
return parseFloat(n.replace(/,/g,''))}
function isAN(n){if(n==='')
return false;if(n==null)
return false;return!isNaN(n);}
function empty_or_undefined(o){if(o==''||typeof o=='undefined')
return true;return false;}
function zero_to_dash(n){if(n==''||n=='0'||typeof n=='undefined'||n=='0.00'||n=='0.000'||n=='-')
return'-';else return n;}
function bra_to_neg(n){console.log(typeof n);if(n=="-"){n="-";}
else if(parseFloat(n)<0){n=Math.abs(parseFloat(n));n='('+n+')';n=n.fontcolor("red");}
return n;}
function empty_to_zero(o){if(o==''||typeof o=='undefined')
return 0;return parseFloat(o);}
function round2(n){return isAN(n)?Math.round(n*100)/100:'';}
function round2z(n){return isAN(n)?rnum(n):0;}
function get_target(e){return $((e.currentTarget)?e.currentTarget:e.srcElement);}
function get_form(e){return $(get_target(e)).closest('form')[0];}
Object.size=function(obj){var size=0,key;for(key in obj){if(obj.hasOwnProperty(key))size++;}
return size;};String.prototype.toCamelCase=function(){return this.replace(/[-_\s]+(.)?/g,function(match,c){return c?c.toUpperCase():"";});}
String.prototype.toUnderscore=function(){return this.replace(/([a-z\d])([A-Z]+)/g,'$1_$2').replace(/[-\s]+/g,'_').toLowerCase();}
String.prototype.toDash=function(){return this.replace(/([A-Z])/g,'-$1').replace(/[-_\s]+/g,'-').toLowerCase();}
String.prototype.toTitleCase=function(){var smallWords=/^(a|an|and|as|at|but|by|en|for|if|in|of|on|or|the|to|vs?\.?|via)$/i;return this.replace(/([^\W_]+[^\s-]*) */g,function(match,p1,index,title){if(index>0&&index+p1.length!==title.length&&p1.search(smallWords)>-1&&title.charAt(index-2)!==":"&&title.charAt(index-1).search(/[^\s-]/)<0){return match.toLowerCase();}
if(p1.substr(1).search(/[A-Z]|\../)>-1){return match;}
return match.charAt(0).toUpperCase()+match.substr(1);});};$(document).on('mouseup mousedown','[contenteditable]',function(){this.focus();});$.ajaxSetup({beforeSend:function(xhr,settings){function getCookie(name){var cookieValue=null;if(document.cookie&&document.cookie!=''){var cookies=document.cookie.split(';');for(var i=0;i<cookies.length;i++){var cookie=jQuery.trim(cookies[i]);if(cookie.substring(0,name.length+1)==(name+'=')){cookieValue=decodeURIComponent(cookie.substring(name.length+1));break;}}}
return cookieValue;}
if(!(/^http:.*/.test(settings.url)||/^https:.*/.test(settings.url))){xhr.setRequestHeader("X-CSRFToken",getCookie('csrftoken'));}}});function TableViewModel(options,row_model,id){var self=this;if(typeof(options.properties)!='undefined'){for(var k in options.properties)
self[k]=options.properties[k];}
self.message=ko.observable();self.state=ko.observable('standby');if(typeof row_model!='undefined'){self.rows=ko.observableArray(ko.utils.arrayMap(options.rows,function(item){return new row_model(item);}));if(self.rows().length){if(typeof self.rows()[0].sn!='undefined'){self.rows().sort(function(l,r){return l.sn()>r.sn()?1:-1});}}
self.deleted_rows=ko.observableArray();self.hasNoRows=ko.computed(function(){return self.rows().length===0;});self.addRow=function(){var new_item_index=self.rows().length+1;self.rows.push(new row_model());arrow_handling();};self.removeRow=function(row){self.rows.remove(row);self.deleted_rows.push(row);};var auto_add_first=true;if(typeof options.auto_add_first!='undefined')
auto_add_first=options.auto_add_first
if(auto_add_first&&self.hasNoRows()){self.addRow();}
self._initial_rows=self.rows().slice(0);self.reset=function(){self.rows(self._initial_rows);}
self.get_total=function(field){var total=0;self.rows().forEach(function(i){if(i){var f=i[field];if(typeof f!='function')
throw new Error(field+' isn\'t a property of row model '+row_model.name+'!')
if(isAN(parseFloat(f())))
total+=parseFloat(f());}});if(typeof rnum=='function'){return rnum(total);}
return total;}}
self.has_real_rows=function(check_by){if(self.rows().length>1)
return true;if(self.rows().length==0)
return false;if(typeof check_by!='undefined'&&self.rows().length==1){if(typeof self.rows()[0][check_by]=='function')
var field=self.rows()[0][check_by]()
else
var field=self.rows()[0][check_by]
if(field)
return true;}
return false;}
if(typeof(options.save_to_url)!='undefined'){self.save=function(model,e){self.state('waiting');var el=get_target(e);if(id!='undefined')$(id).attr('disabled',true);$.ajax({type:"POST",url:options.save_to_url,data:ko.toJSON(self),success:function(msg){self.message('Saved!');self.state('success');if(typeof(options.onSaveSuccess)!='undefined'){options.onSaveSuccess(msg,self.rows());}
self.deleted_rows=[];if(id!='undefined')$(id).attr('disabled',false);},error:function(XMLHttpRequest,textStatus,errorThrown){self.message('Saving Failed!');self.state('error');if(id!='undefined')$(id).attr('disabled',false);}});}}
else{self.save=function(){throw new Error("'save_to_url' option not passed to TableViewModel or save() not implemented!");}}}
function days_between(first,second){var one=new Date(first.getFullYear(),first.getMonth(),first.getDate());var two=new Date(second.getFullYear(),second.getMonth(),second.getDate());var millisecondsPerDay=1000*60*60*24;var millisBetween=two.getTime()-one.getTime();var days=millisBetween/millisecondsPerDay;return Math.floor(days);}
function get_weekday(date){var weekday=new Array(7);weekday[0]="Sunday";weekday[1]="Monday";weekday[2]="Tuesday";weekday[3]="Wednesday";weekday[4]="Thursday";weekday[5]="Friday";weekday[6]="Saturday";return weekday[date.getDay()];}
function hms_to_s(t){var a=t.split(/\D+/);return(a[0]*60+ +a[1])*60+ +a[2]}
bs_alert=function(){}
bs_alert.warning=function(message){$('#alert_placeholder').html('<div class="alert"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')}
bs_alert.error=function(message){$('#alert_placeholder').html('<div class="alert alert-error"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')}
bs_alert.success=function(message){$('#alert_placeholder').html('<div class="alert alert-success"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')}
bs_alert.info=function(message){$('#alert_placeholder').html('<div class="alert alert-info"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')}
bs_alert.clear=function(){$('#alert_placeholder').html('');}
bs_modal=function(){}
bs_modal.create=function(){var el=jQuery('<div/>',{id:'modal'+($('.modal').length+1),class:'modal hide fade'}).appendTo('body');return el;}
function rq(b){var a=function(query){query.callback({results:b});}
return a;}
$(document).ready(function(){$('.nav-tabs li a').click(function(){window.location.hash=$(this).attr('href')});if(window.location.hash){var curr_hash=window.location.hash;var el=$(curr_hash);var to_href=$('a[href="'+curr_hash+'"]').filter(function(){return $(this).data('toggle')=='tab';});if(!$('a[href="'+curr_hash+'"]').filter(function(){return $(this).data('toggle')=='tab';}).is(':visible')){var in_col_box=el.parents('.col-box-body');if(in_col_box.length>0){in_col_box.slideDown();to_href=in_col_box.siblings('.col-box-header')}}
$('html, body').stop().animate({'scrollTop':to_href.offset().top},900,'swing');to_href.tab('show');}});function printDiv(divName){var printContents=document.getElementById(divName).innerHTML;var originalContents=document.body.innerHTML;document.body.innerHTML=printContents;window.print();document.body.innerHTML=originalContents;}
$(document).ready(function(){var elem=$("a").filter(function(){if(this.text=="Profit/Loss")
return this;})
elem.attr('href',"/report/profit-and-loss")})
function BalanceSheet(data){var self=this;self.root_nodes=[];self.asset_total=0.0;self.categories=ko.observableArray(ko.utils.arrayMap(data.categories,function(item){self.root_nodes.push(item.id);return new CategoryViewModel(item);}));self.expandRoot=function(){$('.tree-table').treetable('collapseAll');for(var k in self.root_nodes){$('.tree-table').treetable('expandNode',self.root_nodes[k]);}};}
function CategoryViewModel(data,parent_id){var self=this;self.id=data.id;self.name=data.name;self.parent_id=parent_id;self.accounts=ko.observableArray(ko.utils.arrayMap(data.accounts,function(item){return new AccountViewModel(item,self.id);}));self.categories=ko.observableArray(ko.utils.arrayMap(data.children,function(item){return new CategoryViewModel(item,self.id);}));self.amount=function(){if(this.name=='Total Assets'||this.name=='Total Equity'||this.name=='Total Equity And Liabilities'||this.name=='Total Liabilities')
return data.amt;var total=0;$.each(self.accounts(),function(){if(isAN(this.amount()))
total+=this.amount();});$.each(self.categories(),function(){if(this.name!='Total Assets'&&this.name!='Total Equity'&&this.name!='Total Equity And Liabilities'&&this.name!='Total Liabilities'){if(isAN(this.amount()))
total+=this.amount();}});return total;}
self.cls='category';}
function AccountViewModel(data,parent_id){var self=this;self.id=data.id;self.name=data.name;self.parent_id=parent_id;self.amount=function(){if(isAN(data.amount))
return parseFloat(data.amount);else
return 0;}
self.cls='category';}