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
$(document).ready(function(){$('.date-picker').datepicker();vm=new PurchaseVoucherViewModel(ko_data);ko.applyBindings(vm);});function TaxOptions(name,id){this.name=name;this.id=id;}
function PurchaseVoucherViewModel(data){var self=this;self.tax_options=ko.observableArray([new TaxOptions('Tax Inclusive','inclusive'),new TaxOptions('Tax Exclusive','exclusive'),new TaxOptions('No Tax','no')]);$.ajax({url:'/inventory/items/json/',dataType:'json',async:false,success:function(data){self.items=data;}});$.ajax({url:'/ledger/party/suppliers.json',dataType:'json',async:false,success:function(data){self.suppliers=data;}});$.ajax({url:'/tax/schemes/json/',dataType:'json',async:false,success:function(data){self.tax_schemes=data;}});self.tax_scheme_by_id=function(id){var scheme=$.grep(self.tax_schemes,function(i){return i.id==id;});return scheme[0];}
$.ajax({url:'/ledger/accounts.json',dataType:'json',async:false,success:function(data){self.accounts=data;}});self.party=ko.observable();self.description=ko.observable();for(var k in data)
self[k]=data[k];self.tax=ko.observable(data['tax']);self.id=ko.observable(data['id']);self.status=ko.observable(data['status']);self.message=ko.observable('');self.state=ko.observable('standby');self.party_address=ko.observable('');self.accounts_by_category=function(categories,is_or){var filtered_accounts=[];for(var i in self.accounts){var account_categories=self.accounts[i].categories;if(typeof categories==='string'){if($.inArray(categories,account_categories)!==-1){filtered_accounts.push(self.accounts[i]);}}else if(typeof is_or!='undefined'){if(intersection(categories,account_categories).length){filtered_accounts.push(self.accounts[i]);}}else{if(compare_arrays(categories,account_categories)){filtered_accounts.push(self.accounts[i]);}}}
return filtered_accounts;};var options={rows:data.particulars};self.particulars=new TableViewModel(options,ParticularViewModel);self.validate=function(){var rows=self.particulars.rows();if(rows.length==0){bs_alert.error('No rows to save.');return false;}
else{for(var i=0;i<rows.length;i++){if(!rows[i].validate()){return false;}}
return true;}}
self.save=function(item,event){if(!self.validate()){return false;}
var formdata=new FormData();var file=$('#id_attachment')[0].files[0];formdata.append('data',ko.toJSON(self));formdata.append('attachment',file);$.ajax({type:"POST",url:'/voucher/purchase-voucher/save/',data:formdata,processData:false,contentType:false,success:function(msg){if(typeof(msg.error_message)!='undefined'){$('#message').html(msg.error_message);}
else{bs_alert.success('Saved!');if(msg.id)
self.id=msg.id;window.location='/voucher/purchase-voucher/'+msg.id;}},error:console.log('error is occured')});}
self.save_continue=function(item,event){if(!self.validate()){return false;}
var formdata=new FormData();var file=$('#id_attachment')[0].files[0];formdata.append('data',ko.toJSON(self));formdata.append('attachment',file);$.ajax({type:"POST",url:'/voucher/purchase-voucher/save/',data:formdata,processData:false,contentType:false,success:function(msg){if(typeof(msg.error_message)!='undefined'){$('#message').html(msg.error_message);}
else{bs_alert.success('Saved!');window.location='/voucher/purchase-voucher/';}},error:console.log('error is occured')});}
self.sub_total=function(){var sum=0;self.particulars.rows().forEach(function(i){sum+=i.amount();});return rnum(sum);}
self.tax_amount=function(){var sum=0;self.particulars.rows().forEach(function(i){if(typeof self.tax_scheme_by_id(i.tax_scheme())!='undefined'){var tax_percent=self.tax_scheme_by_id(i.tax_scheme()).percent;var tax_amount=i.amount()*(tax_percent/100);sum+=tax_amount;}});return rnum(sum);}
self.validate=function(){bs_alert.clear();if(!self.party){bs_alert.error('"From" field is required!');self.state('error');return false;}
var rows=self.particulars.rows();if(rows.length==0){bs_alert.error('No rows to save.');}
else{for(var i=0;i<rows.length;i++){if(!rows[i].validate()){return false;}}}
return true;}
self.itemChanged=function(row){var selected_item=$.grep(self.items,function(i){return i.id==row.item_id();})[0];if(!selected_item)return;if(!row.description())
row.description(selected_item.description);if(!row.tax_scheme())
row.tax_scheme(selected_item.tax_scheme);}
self.supplier_changed=function(vm){var selected_obj=$.grep(self.suppliers,function(i){return i.id==vm.party;})[0];self.party_address(selected_obj.address);}
self.particulars.grand_total=ko.computed(function(){return self.sub_total()+self.tax_amount();return rnum(self.sub_total());},self);self.approve=function(item,event){if(!self.validate())
return false;if(get_form(event).checkValidity()){$.ajax({type:"POST",url:'/voucher/purchase-voucher/approve/',data:ko.toJSON(self),success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);}
else{bs_alert.success('Approved!')
self.status('Approved');self.state('success');}
window.location='/voucher/purchase-voucher/'+self.id();}});}
else
return true;}
self.unapprove=function(item,event){if(!self.validate())
return false;if(get_form(event).checkValidity()){$.ajax({type:"POST",url:'/voucher/purchase-voucher/unapprove/'+self.id()+'/',data:ko.toJSON(self),success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);}
else{bs_alert.success('Unapproved!')
self.status('Unapproved');self.state('success');}
window.location='/voucher/purchase-voucher/'+self.id();}});}
else
return true;}}
function ParticularViewModel(particular){var self=this;self.account=ko.observable();self.description=ko.observable();self.unit_price=ko.observable(0);self.quantity=ko.observable(1);self.discount=ko.observable(0).extend({numeric:2});self.tax_scheme=ko.observable();for(var k in particular)
self[k]=ko.observable(particular[k]);if(self.discount()==null)
self.discount(0);self.amount=ko.computed(function(){var wo_discount=self.quantity()*self.unit_price();var amt=wo_discount-((self.discount()*wo_discount)/100);return amt;});self.validate=function(){if(!self.account()){bs_alert.error('Particular is not allowed to be empty');return false;}
else if(!self.unit_price()){bs_alert.error('Price is not allowed to be empty.');return false;}
else if(!self.quantity()){bs_alert.error('Quantity is not allowed to be empty.');return false;}
else{return true;}}}