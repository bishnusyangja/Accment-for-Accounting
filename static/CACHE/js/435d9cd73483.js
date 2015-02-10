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
var datas={'#transfer-table':2,'#cash-sales-table':1,'#lotto-sales-table':1,'#actual-sales-table':2,'#sales-through-cards-table':2,'#sales-through-others-table':1,'#vendor-payout-table':2,'#other-payout-table':2,'#vendor-charge-table':2,'#deposit-table':2,'#lotto-fixed-header':5,'#fuel-table':3,'#other-inventory-table':3,'#journal-voucher-table':3,'#bank-deposit-table':3,'#bank-payment-table':3,'#cash-receipt-table':3,'#cash-payment-table':3,'#physical-stock-voucher-table':3,'#work-time-voucher-table':6,'#group-payroll-table':5,'#asset-code-table':9,'#asset-ledger-table':2,'#hour-attendance-table':6,"#scratch-off-latest-table":4}
var locn=null;function arrow_handling(){$('input[target="inside_td"]').bind("keyup",function(event){var index=$("input[target='inside_td']").index(event.target);a="#"+$(this).parent('td').parent('tr').parent('tbody').parent('table').attr('id');locn=datas[a];switch(event.keyCode){case 37:index--;if(index<0)break;$("input[target='inside_td']")[index].focus();break;case 39:index++;$("input[target='inside_td']")[index].focus();break;case 38:for(var i=0;i<locn;i++)
index--;if(index<0)break;$("input[target='inside_td']")[index].focus();break;case 40:for(var i=0;i<locn;i++)
index++;$("input[target='inside_td']")[index].focus();break;}
event.preventDefault();});}
arrow_handling();$(document).ready(function(){$('.date-picker').datepicker().data('datepicker');vm=new JournalVoucher(ko_data);ko.applyBindings(vm);});function JournalVoucher(data){var self=this;self.date='';for(var k in data)
self[k]=data[k];self.id=ko.observable(data['id']);self.status=ko.observable(data['status']);self.attachment=ko.observable();$.ajax({url:'/ledger/accounts.json',dataType:'json',async:false,success:function(data){self.accounts=data;}});self.accounts_except_category=function(categories,is_or){var filtered_accounts=[];for(var i in self.accounts){var account_categories=self.accounts[i].categories;if(typeof categories==='string'){if($.inArray(categories,account_categories)==-1){filtered_accounts.push(self.accounts[i]);}}else if(typeof is_or!='undefined'){if(!intersection(categories,account_categories).length){filtered_accounts.push(self.accounts[i]);}}else{if(!compare_arrays(categories,account_categories)){filtered_accounts.push(self.accounts[i]);}}}
return filtered_accounts;};var validate=function(msg,rows,tr_wrapper_id){var selection=$("#"+tr_wrapper_id+" > tr");selection.each(function(index){$(selection[index]).addClass('invalid-row');});for(var i in msg['saved']){rows[i].id=msg['saved'][''+i+''];$(selection[i]).removeClass('invalid-row');}
var model=self[tr_wrapper_id.toUnderscore()];var saved_size=Object.size(msg['saved']);if(saved_size==rows.length)
model.message('Saved!');else if(saved_size==0){model.message('No rows saved!');model.status('error');}
else if(saved_size<rows.length){var message=saved_size.toString()+' row'+((saved_size==1)?'':'s')+' saved! ';message+=(rows.length-saved_size).toString()+' row'+((rows.length-saved_size==1)?' is':'s are')+' incomplete!';model.message(message);model.status('error');}}
var key_to_options=function(key){return{rows:data['rows'],save_to_url:'/voucher/journal/save/',properties:{id:self.id},onSaveSuccess:function(msg,rows){validate(msg,rows,key.toDash());}};}
self.journal_voucher=new TableViewModel(key_to_options('journal_voucher'),JournalVoucherRow);self.journal_voucher.cr_total=ko.computed(function(){var total=0.00;$.each(self.journal_voucher.rows(),function(){if(isAN(this.cr_amt())){total+=parseFloat(this.cr_amt());}});return rnum(total);},self);self.journal_voucher.dr_total=ko.computed(function(){var total=0.00;$.each(self.journal_voucher.rows(),function(){if(isAN(this.dr_amt()))
total+=parseFloat(this.dr_amt());});return rnum(total);},self);self.add_row=function(element,viewModel){$(element).blur();var type;var dr_amount;var cr_amount;var diff=self.journal_voucher.dr_total()-self.journal_voucher.cr_total()
if(diff>0){type='Cr';dr_amount=0;cr_amount=diff;}else{type='Dr';cr_amount=0;dr_amount=(-1)*diff;}
if($(element).closest("tr").is(":nth-last-child(2)")&&self.journal_voucher.dr_total()!=self.journal_voucher.cr_total())
self.journal_voucher.rows.push(new JournalVoucherRow({type:type,cr_amount:cr_amount,dr_amount:dr_amount}));}
self.journal_voucher.cr_equals_dr=function(){return self.journal_voucher.dr_total()===self.journal_voucher.cr_total();}
self.journal_voucher.total_row_class=function(){if(self.journal_voucher.dr_total()===self.journal_voucher.cr_total())
return'valid-row';return'invalid-row';}
self.journal_voucher.approve=function(){$.ajax({type:"POST",url:'/voucher/journal/approve/',data:ko.toJSON(self),success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);}
else{bs_alert.success('Approved!');self.status('Approved');self.journal_voucher.state('success');}}});}
self.journal_voucher.cancel=function(item,event){$.ajax({type:"POST",url:'/voucher/journal/cancel/',data:ko.toJSON(self),success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);}
else{bs_alert.success('Cancelled!');self.status('Cancelled');self.journal_voucher.state('success');if(msg.id)
self.id(msg.id);}}});}
self.journal_voucher.save=function(item,event){self.journal_voucher.state('waiting');var valid=true;var message='';var rows=self.journal_voucher.rows();var selection=$("#journal-voucher > tr");var formdata=new FormData();var file=$('#attachment')[0].files[0];formdata.append('attachment',file);formdata.append('data',ko.toJSON(self));if(!self.journal_voucher.cr_equals_dr()){message+='Total Dr and Cr amounts don\'t tally!<br/>';valid=false;}
for(var i=0;i<self.journal_voucher.rows().length;i++){if(!self.journal_voucher.rows()[i].has_particulars()){if(message.length==0)
message+='Particular is not allowed to be empty!<br/>'
valid=false;break;}}
var temp_acc=[];for(var i=0;i<self.journal_voucher.rows().length;i++){if(self.journal_voucher.rows()[i].has_particulars()){if(temp_acc.indexOf(self.journal_voucher.rows()[i].account())>=0){valid=false;message+='Duplicated Particulars Not Allowed!'
break;}
else{temp_acc.push(self.journal_voucher.rows()[i].account());}}}
if(!valid){self.journal_voucher.state('error');bs_alert.error(message);return false;}
if(get_form(event).checkValidity()){if($(get_target(event)).data('continue')){self.continue=true;formdata.append('continue',self.continue);}
$.ajax({type:"POST",url:'/voucher/journal/save/',async:false,processData:false,contentType:false,cache:false,data:formdata,success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);}
else{bs_alert.success('Saved!');self.deleted_rows=[];self.journal_voucher.state('success');if(msg.id){self.id(msg.id);self.status('Unapproved');}}},error:function(XMLHttpRequest,textStatus,errorThrown){bs_alert.error('Saving Failed!');self.journal_voucher.state('error');}});}
else
return true;}}
function JournalVoucherRow(row){var self=this;var selected=$('#selection :selected').text();self.type=ko.observable(selected);self.account=ko.observable();self.description=ko.observable();self.dr_amount=ko.observable();self.cr_amount=ko.observable();self.id=ko.observable();self.is_dr=function(){if(self.type()=='Dr'){return true;}
return false;}
self.is_cr=function(){if(self.type()=='Cr'){return true}
return false;}
self.dr_amt=function(){if(this.is_dr())
return self.dr_amount();return 0.00;}
self.has_particulars=function(){if(typeof(self.account())!='undefined')
return true;else
return false;}
self.cr_amt=function(){if(this.is_cr())
return this.cr_amount();return 0.00;}
self.type_changed=function(e){}
for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}