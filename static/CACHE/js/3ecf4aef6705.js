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
$(document).ready(function(){$(document).ready(function(){$('.date-picker').datepicker({endDate:'0d'});});if(scenario=='Create'){$('#group-payroll-table').hide();$('.btn').hide();}
vm=new GroupPayrollVoucherVM(ko_data);ko.applyBindings(vm);$('.change-on-ready').trigger('change');});function GroupPayrollVoucherVM(data){var self=this;$.ajax({url:'/payroll/employees.json',dataType:'json',async:false,success:function(data){self.employees=data;}});$.ajax({url:'/ledger/payheads.json',dataType:'json',async:false,success:function(data){self.accounts=data;}});self.id=ko.observable();self.message=ko.observable();self.state=ko.observable('standby');self.voucher_no=ko.observable();self.date=ko.observable();self.from_date=ko.observable();self.to_date=ko.observable();self.date_range=function(){if(self.from_date()&&self.to_date()){$('#group-payroll-table').show();$('.btn').show();}
else
return;}
for(var k in data){if(data[k])
self[k]=ko.observable(data[k]);}
var options={rows:data.rows}
self.table_vm=new TableViewModel(options,GroupPayrollVoucherRowVM);self.check_valid=function(){if(!self.date()){bs_alert.error('Date is not allowed to be empty !');return false;}else if(!self.voucher_no()){bs_alert.error('Voucher Number is not allowed to be empty !');return false;}else if(!self.from_date()){bs_alert.error('From Date is not allowed to be empty !');return false;}else if(!self.to_date()){bs_alert.error('To Date is not allowed to be empty !');return false;}else{console.log('');}
len=self.table_vm.rows();for(var i=0;i<len.length;i++){var temp_count=0;for(var j=0;j<len.length;j++){if(len[i].employee()==len[j].employee()){if(temp_count==1){var emp=$.grep(self.employees,function(e){return e.id==len[i].employee();})[0];bs_alert.error('Multiple Employees with name 'emp.name+' are not allowed !');return false;}
temp_count+=1;}}
if(!len[i].employee()){bs_alert.error('Employee is not allowed to be empty !');return false;}else if(!len[i].rate_day()){bs_alert.error('Day Rate is not allowed to be empty !');return false;}else if(!len[i].rate_hour()){bs_alert.error('Hour Rate is not allowed to be empty !');return false;}else if(!len[i].pay_head()){bs_alert.error('Pay Head is not allowed to be empty !');return false;}else{console.log('');}}
return true;}
self.save=function(item,event){if(get_form(event).checkValidity()){if($(get_target(event)).data('continue')){self.continue=true;}
if(!self.check_valid()){return false;}
var data=ko.toJSON(self);$.ajax({type:"POST",url:'/payroll/group-voucher/save/',data:data,success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);self.state('error');}
else{bs_alert.success('Saved!');self.state('success');if(msg.id){self.id(msg.id);self.status('Unapproved');}
for(var i in msg.rows){self.table_vm.rows()[i].id=msg.rows[i];}
if(msg.redirect_to){window.location=msg.redirect_to;}else{window.location='/payroll/group-voucher/'+msg.id+'/'}}}});}
else
return true;}
self.approve=function(item,event){$.ajax({type:"POST",url:'/payroll/group-voucher/approve/',data:ko.toJSON(self),success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);self.state('error');}
else{bs_alert.success('Approved!');self.state('success');self.status('Approved');if(msg.id)
self.id(msg.id);window.location=msg.redirect_to;}}});}
self.unapprove=function(item,event){$.ajax({type:"POST",url:'/payroll/group-voucher/unapprove/'+self.id()+'/',data:ko.toJSON(self),success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);self.state('error');}
else{bs_alert.success('Unapproved!');self.state('success');self.status('Unapproved');if(msg.id)
self.id(msg.id);window.location=msg.redirect_to;}}});}}
function GroupPayrollVoucherRowVM(data){var self=this;self.employee=ko.observable();self.present_days=ko.observable();self.present_hours=ko.observable();self.present_ot_hours=ko.observable();self.rate_day=ko.observable();self.rate_hour=ko.observable();self.rate_ot_hour=ko.observable();self.payroll_tax=ko.observable();self.pay_head=ko.observable();for(var k in data)
if(data[k])
self[k]=ko.observable(data[k]);self.employee_changed=function(row){if(approved==1)return;var selected_item=$.grep(vm.employees,function(i){return i.id==row.employee();})[0];if(!selected_item)return;$.ajax({type:"POST",url:'/payroll/employee-detail/',dataType:'html',data:{'employee':selected_item.id,'start':vm.from_date,'end':vm.to_date},success:function(data){data=$.parseJSON(data);self.present_hours(data.worked_hours);self.present_days(data.worked_days);}});}
self.amount=ko.computed(function(){return(round2z(self.present_days())*round2z(self.rate_day())+round2z(self.present_hours())*round2z(self.rate_hour())).toFixed(2);});self.net=ko.computed(function(){return(self.amount()-round2z(self.payroll_tax())).toFixed(2);});self.is_valid=function(){if(self.net()<0.0)return false;else return true;};self.style=function(){if(self.net()<0.0)return"invalid-row";else return"valid-row";};}
var datas={'#transfer-table':2,'#cash-sales-table':1,'#lotto-sales-table':1,'#actual-sales-table':2,'#sales-through-cards-table':2,'#sales-through-others-table':1,'#vendor-payout-table':2,'#other-payout-table':2,'#vendor-charge-table':2,'#deposit-table':2,'#lotto-fixed-header':5,'#fuel-table':3,'#other-inventory-table':3,'#journal-voucher-table':3,'#bank-deposit-table':3,'#bank-payment-table':3,'#cash-receipt-table':3,'#cash-payment-table':3,'#physical-stock-voucher-table':3,'#work-time-voucher-table':6,'#group-payroll-table':5,'#asset-code-table':9,'#asset-ledger-table':2,'#hour-attendance-table':6,"#scratch-off-latest-table":4}
var locn=null;function arrow_handling(){$('input[target="inside_td"]').bind("keyup",function(event){var index=$("input[target='inside_td']").index(event.target);a="#"+$(this).parent('td').parent('tr').parent('tbody').parent('table').attr('id');locn=datas[a];switch(event.keyCode){case 37:index--;if(index<0)break;$("input[target='inside_td']")[index].focus();break;case 39:index++;$("input[target='inside_td']")[index].focus();break;case 38:for(var i=0;i<locn;i++)
index--;if(index<0)break;$("input[target='inside_td']")[index].focus();break;case 40:for(var i=0;i<locn;i++)
index++;$("input[target='inside_td']")[index].focus();break;}
event.preventDefault();});}
arrow_handling();