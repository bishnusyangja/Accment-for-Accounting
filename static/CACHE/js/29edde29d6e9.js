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
$(document).ready(function(){$(document).ready(function(){$('.date-picker').datepicker({endDate:'0d'});});vm=new IndividualPayrollVoucherVM(ko_data);ko.applyBindings(vm);$('.change-on-ready').trigger('change');});function IndividualPayrollVoucherVM(data){var self=this;self.valid=ko.observable(true);$.ajax({url:'/payroll/employees.json',dataType:'json',async:false,success:function(data){self.employees=data;}});$.ajax({url:'/ledger/accounts.json',dataType:'json',async:false,success:function(data){self.accounts=data;}});self.id=ko.observable();self.message=ko.observable();self.state=ko.observable('standby');self.voucher_no=ko.observable();self.date=ko.observable();self.employee=ko.observable();self.days_worked=ko.observable();self.hours_worked=ko.observable();self.ot_hours_worked=ko.observable();self.day_rate=ko.observable();self.hour_rate=ko.observable();self.ot_hour_rate=ko.observable();self.from_date=ko.observable();self.to_date=ko.observable();for(var k in data){if(data[k])
self[k]=ko.observable(data[k]);}
self.employee_changed=function(data){if(approved==1)return;var selected_item=$.grep(self.employees,function(i){return i.id==data.employee();})[0];if(!selected_item)return;if(!self.to_date()||!self.employee())
return;$.ajax({type:"POST",url:'/payroll/employee-detail/',dataType:'html',data:{'employee':selected_item.id,'end':self.to_date},success:function(data){data=$.parseJSON(data);self.hours_worked(data.worked_hours);self.days_worked(data.worked_days);self.from_date(data.start);}});}
self.day_amount=function(){var value=self.days_worked()*self.day_rate();value=isNaN(value)?0:value;return value;}
self.hour_amount=function(){var value=(self.hours_worked()*self.hour_rate());value=isNaN(value)?0:value;return value;}
self.total=function(){var value=(self.day_amount())+(self.hour_amount());value=isNaN(value)?0:value;return value;}
self.accounts_by_category=function(categories,is_or){var filtered_accounts=[];for(var i in self.accounts){var account_categories=self.accounts[i].categories
if(typeof categories==='string'){if($.inArray(categories,account_categories)!==-1){filtered_accounts.push(self.accounts[i]);}}else if(typeof is_or!='undefined'){if(intersection(categories,account_categories).length){filtered_accounts.push(self.accounts[i]);}}else{if(compare_arrays(categories,account_categories)){filtered_accounts.push(self.accounts[i]);}}}
return filtered_accounts;};self.inclusions=new TableViewModel({rows:data.inclusions},IndividualPayrollVoucherRowVM);self.deductions=new TableViewModel({rows:data.deductions},IndividualPayrollVoucherRowVM);self.validate=function(){bs_alert.clear()
if(!self.employee()){bs_alert.error('"Employee" is required!')
self.state('error');return false;}
return true;}
self.check_valid=function(){if(self.day_rate()&&self.hour_rate()&&self.voucher_no()&&self.date()&&self.employee()&&self.to_date()){var val=self.inclusions.rows();if(val.length>0){for(var i=0;i<val.length;i++){if(!val[i].check_valid()){self.valid(false);break;}
else{self.valid(true);}}}
else{self.valid(true);}
if(self.valid()){var val=self.deductions.rows();if(val.length>0){for(var i=0;i<val.length;i++){if(!val[i].check_valid()){self.valid(false);break;}
else{self.valid(true);}}}
else{self.valid(true);}}}
return self.valid();}
self.save=function(item,event){if(!self.validate())
return false;console.log(self.check_valid())
if(!self.check_valid()){bs_alert.error("Fields are not allowed to be empty.");return false;}
if(get_form(event).checkValidity()){if($(get_target(event)).data('continue')){self.continue=true;}
var data=ko.toJSON(self);$.ajax({type:"POST",url:'/payroll/individual-voucher/save/',data:data,success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);self.state('error');}
else{bs_alert.success('Saved!');self.state('success');if(msg.id){self.id(msg.id);self.status('Unapproved');}
if(msg.redirect_to){window.location=msg.redirect_to;}
$("#table-body-inclusions > tr").each(function(i){$($("#table-body-inclusions > tr")[i]).addClass('invalid-row');});$("#table-body-deductions > tr").each(function(i){$($("#table-body-deductions > tr")[i]).addClass('invalid-row');});for(var i in msg.rows1){self.inclusions.rows()[i].id=msg.rows1[i];$($("#table-body-inclusions > tr")[i]).removeClass('invalid-row');}
for(var i in msg.rows2){self.deductions.rows()[i].id=msg.rows2[i];$($("#table-body-deductions > tr")[i]).removeClass('invalid-row');}
if(msg.redirect_to){window.location=msg.redirect_to;}else{window.location='/payroll/individual-voucher/'+msg.id+'/'}}}});}
else
return true;}
self.approve=function(item,event){$.ajax({type:"POST",url:'/payroll/individual-voucher/approve/',data:ko.toJSON(self),success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);self.state('error');}
else{bs_alert.success('Approved!');self.state('success');self.status('Approved');if(msg.id)
self.id(msg.id);window.location=msg.redirect_to;}}});}
self.unapprove=function(item,event){$.ajax({type:"POST",url:'/payroll/individual-voucher/unapprove/'+self.id()+'/',data:ko.toJSON(self),success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);self.state('error');}
else{bs_alert.success('Unpproved!');self.state('success');self.status('Unapproved');if(msg.id)
self.id(msg.id);window.location=msg.redirect_to;}}});}}
function IndividualPayrollVoucherRowVM(data){var self=this;self.account=ko.observable();self.amount=ko.observable();for(var k in data){if(data[k])
self[k]=ko.observable(data[k]);}
self.check_valid=function(){if(self.account()&&self.amount()){return true;}
else{return false;}}}
function deepcopy(obj){if(Object.prototype.toString.call(obj)==='[object Array]'){var out=[],i=0,len=obj.length;for(;i<len;i++){out[i]=arguments.callee(obj[i]);}
return out;}
if(typeof obj==='object'){var out={},i;for(i in obj){out[i]=arguments.callee(obj[i]);}
return out;}
return obj;}