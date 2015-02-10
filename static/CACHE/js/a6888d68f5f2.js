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
function TrialBalance(data){var self=this;self.root_nodes=[];self.categories=ko.observableArray(ko.utils.arrayMap(data.categories,function(item){self.root_nodes.push(item.id);return new CategoryViewModel(item);}));self.option_show_zero_balance_ledger=ko.observable(false);self.option_net_view=ko.observable(true);self.option_transactions_view=ko.observable(true);self.option_opening_view=ko.observable(true);self.expandRoot=function(){$('.tree-table').treetable('collapseAll');for(var k in self.root_nodes){$('.tree-table').treetable('expandNode',self.root_nodes[k]);}};self.opening_dr_total=function(){var total=0;$.each(self.categories(),function(){if(isAN(this.net_opening_dr()))
total+=this.net_opening_dr();});return total;};self.opening_cr_total=function(){var total=0;$.each(self.categories(),function(){if(isAN(this.net_opening_cr()))
total+=this.net_opening_cr();});return total;};self.transaction_dr_total=function(){var total=0;$.each(self.categories(),function(){if(isAN(this.transaction_dr()))
total+=this.transaction_dr();});return total;};self.transaction_cr_total=function(){var total=0;$.each(self.categories(),function(){if(isAN(this.transaction_cr()))
total+=this.transaction_cr();});return total;};self.net_transaction_dr_total=function(){var total=0;$.each(self.categories(),function(){if(isAN(this.net_transaction_dr()))
total+=this.net_transaction_dr();});return total;};self.net_transaction_cr_total=function(){var total=0;$.each(self.categories(),function(){if(isAN(this.net_transaction_cr()))
total+=this.net_transaction_cr();});return total;};self.dr_total=function(){var total=0;$.each(self.categories(),function(){if(isAN(this.net_dr()))
total+=this.net_dr();});return total;};self.cr_total=function(){var total=0;$.each(self.categories(),function(){if(isAN(this.net_cr()))
total+=this.net_cr();});return total;};self.balanced=function(){return self.cr_total()==self.dr_total();};}
function CategoryViewModel(data,parent_id){var self=this;self.id=data.id;self.name=data.name;self.parent_id=parent_id;self.accounts=ko.observableArray(ko.utils.arrayMap(data.accounts,function(item){return new AccountViewModel(item,self.id);}));self.categories=ko.observableArray(ko.utils.arrayMap(data.children,function(item){return new CategoryViewModel(item,self.id);}));self.opening_dr=function(){var total=0;$.each(self.accounts(),function(){if(isAN(this.opening_dr()))
total+=this.opening_dr();});$.each(self.categories(),function(){if(isAN(this.opening_dr()))
total+=this.opening_dr();});return total;}
self.opening_cr=function(){var total=0;$.each(self.accounts(),function(){if(isAN(this.opening_cr()))
total+=this.opening_cr();});$.each(self.categories(),function(){if(isAN(this.opening_cr()))
total+=this.opening_cr();});return total;}
self.net_opening_cr=function(){if(self.opening_cr()>self.opening_dr())
return self.opening_cr()-self.opening_dr();else
return 0;}
self.net_opening_dr=function(){if(self.opening_dr()>=self.opening_cr())
return self.opening_dr()-self.opening_cr();else
return 0;}
self.closing_dr=function(){var total=0;$.each(self.accounts(),function(){if(isAN(this.closing_dr()))
total+=this.closing_dr();});$.each(self.categories(),function(){if(isAN(this.closing_dr()))
total+=this.closing_dr();});return total;}
self.closing_cr=function(){var total=0;$.each(self.accounts(),function(){if(isAN(this.closing_cr()))
total+=this.closing_cr();});$.each(self.categories(),function(){if(isAN(this.closing_cr()))
total+=this.closing_cr();});return total;}
self.transaction_dr=function(){var total=0;$.each(self.accounts(),function(){if(isAN(this.transaction_dr()))
total+=this.transaction_dr();});$.each(self.categories(),function(){if(isAN(this.transaction_dr()))
total+=this.transaction_dr();});return total;}
self.transaction_cr=function(){var total=0;$.each(self.accounts(),function(){if(isAN(this.transaction_cr()))
total+=this.transaction_cr();});$.each(self.categories(),function(){if(isAN(this.transaction_cr()))
total+=this.transaction_cr();});return total;}
self.net_dr=function(){if(self.closing_dr()>self.closing_cr())
return self.closing_dr()-self.closing_cr();return 0;}
self.net_cr=function(){if(self.closing_cr()>self.closing_dr())
return self.closing_cr()-self.closing_dr();return 0;}
self.net_transaction_dr=function(){if(self.transaction_dr()>self.transaction_cr())
return self.transaction_dr()-self.transaction_cr();return 0;}
self.net_transaction_cr=function(){if(self.transaction_cr()>self.transaction_dr())
return self.transaction_cr()-self.transaction_dr();return 0;}
self.cls='category';}
function AccountViewModel(data,parent_id){var self=this;self.id=data.id;self.name=data.name;self.parent_id=parent_id;self.opening_credit=ko.observable(data.opening_cr);self.opening_debit=ko.observable(data.opening_dr);self.closing_credit=ko.observable(data.closing_cr);self.closing_debit=ko.observable(data.closing_dr);self.transaction_credit=ko.observable(data.transaction_cr);self.transaction_debit=ko.observable(data.transaction_dr);self.opening_cr=function(){if(isAN(self.opening_credit()))
return parseFloat(self.opening_credit());else
return 0;}
self.opening_dr=function(){if(isAN(self.opening_debit()))
return parseFloat(self.opening_debit());else
return 0;}
self.closing_cr=function(){if(isAN(self.closing_credit()))
return parseFloat(self.closing_credit());else
return 0;}
self.closing_dr=function(){if(isAN(self.closing_debit()))
return parseFloat(self.closing_debit());else
return 0;}
self.transaction_cr=function(){if(isAN(self.transaction_credit()))
return parseFloat(self.transaction_credit());else
return 0;}
self.transaction_dr=function(){if(isAN(self.transaction_debit()))
return parseFloat(self.transaction_debit());else
return 0;}
self.net_opening_cr=function(){if(self.opening_cr()>self.opening_dr())
return self.opening_cr()-self.opening_dr();else
return 0;}
self.net_opening_dr=function(){if(self.opening_dr()>=self.opening_cr())
return self.opening_dr()-self.opening_cr();else
return 0;}
self.net_dr=function(){if(self.closing_dr()>=self.closing_cr()){return self.closing_dr()-self.closing_cr();}
return 0;}
self.net_cr=function(){if(self.closing_cr()>self.closing_dr()){return self.closing_cr()-self.closing_dr();}
return 0;}
self.net_transaction_dr=function(){if(self.transaction_dr()>=self.transaction_cr()){return self.closing_dr()-self.closing_cr();}
return 0;}
self.net_transaction_cr=function(){if(self.transaction_cr()>self.transaction_dr()){return self.transaction_cr()-self.transaction_dr();}
return 0;}
self.isVisible=function(){return false;}
if((self.net_cr()==''||self.net_cr()==null||self.net_cr=='0')&&(self.net_dr()==''||self.net_dr()==null||self.net_dr=='0')){self.cls='category';}else{self.cls='category';}}