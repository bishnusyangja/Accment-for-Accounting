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
$(document).ready(function(){vm=new DayJournal(ko_data);ko.applyBindings(vm);$('.change-on-ready').trigger('change');if(window.location.hash!=""){$('a[href="'+window.location.hash+'"]').click();}
$(document).on("click",".delete-attachment",function(e){e.preventDefault();var $this=$(this);if(confirm("Are you sure you want to delete this attachment?")){var uri=build_attachment_url($this.data("type"),$this.data('id'));$.post(uri.url,uri.params).done(function(res){if(res.success){$this.parent('.span3').fadeOut(300,function(){$(this).remove();});}else{alert("There has been error while processing your request. Please try again!");}});}else{return false;}});function build_attachment_url(type,id){return{url:"/day/delete_attachment/",params:{type:type,id:id}};}
var add_file_view=$('.attach_file_field').first();$('#clear-other-attachment').on('click',function(){clearFileInput("other-attachment");});$('#clear-sales-attachment').on('click',function(){clearFileInput("sales-attachment");});$('#clear-bank-attachment').on('click',function(){clearFileInput("bank-attachment");});$('#clear-purchase-attachment').on('click',function(){clearFileInput("purchase-attachment");});$('.add_file').click(function(){var _parent=$(this).parent('p');var clone=add_file_view.clone();clone.append('<button type="button" class="btn btn-danger pull-right remove-file-attach">X</button>')
clone.find('input').val("");_parent.before(clone);});$(document).on('click','.remove-file-attach',function(){$(this).parent('.attach_file_field').slideUp(400,function(){$(this).remove()});});$('.attachment-form').submit(function(e){e.preventDefault();var save_button=$(this).find('input[value="Save"]').attr('id')
$("#"+save_button).attr('disabled','true');console.log("BEFORE ",$("#"+save_button));if(window.FormData){var file_ips=$(this).find('input[type="file"]');var text_ips=$(this).find('.captions');var formdata=new FormData();$.each(text_ips,function(){formdata.append("captions",this.value);});$.each(file_ips,function(){formdata.append("attachments",this.files[0]);});var $this=$(this);var type=$this.data("type");formdata.append("type",type);formdata.append("day",$('#attachment_tabbable').data("journal-day"));$.ajax({url:"/day/save_attachments/",type:"POST",data:formdata,processData:false,contentType:false,success:function(res){var str="";$.each(res,function(){str+='<div class="span3"> <a target="_blank" href="'+this.link+'">'+this.caption+'</a><button class="close delete-attachment" data-type="'+type+'" data-id="'+this.id+'"><span class="icon-trash"></span></button></div>';});$this.find('.row-fluid').append(str);$this.find('.attach_file_field').find("input").val("").end().not(':first').remove();},error:function(){alert("There has been error while processing your request. Please try again!");}});$("#"+save_button).removeAttr('disabled');console.log("AFTER ",$("#"+save_button));}else{alert("Your browser is too old. Please upgrade to modern browsers like Chrome or Firefox.")}});});function clearFileInput(id){var oldInput=document.getElementById(id);var newInput=document.createElement("input");newInput.type="file";newInput.id=oldInput.id;newInput.name=oldInput.name;newInput.className=oldInput.className;newInput.style.cssText=oldInput.style.cssText;oldInput.parentNode.replaceChild(newInput,oldInput);}
function DayJournal(data){var self=this;self.sales_tax=ko.observable();self.state=ko.observable();for(var k in data)
self[k]=data[k];self.voucher_no=ko.observable();if(data['voucher_no']){self.voucher_no(data['voucher_no']);}
self.status=ko.observable();if(data['status']){self.status(data['status']);}
self.lotto_sales_dispenser_amount=ko.observable(0.00);if(isAN(data['lotto_sales_dispenser_amount'])){self.lotto_sales_dispenser_amount(rnum(parseFloat(data['lotto_sales_dispenser_amount'])));}
self.lotto_sales_register_amount=ko.observable(0.00);if(data['lotto_sales_register_amount']){self.lotto_sales_register_amount(rnum(parseFloat(data['lotto_sales_register_amount'])));}
self.scratch_off_sales_register_amount=ko.observable(0.00);if(data['scratch_off_sales_register_amount']){self.scratch_off_sales_register_amount(rnum(parseFloat(data['scratch_off_sales_register_amount'])));}
self.register_sales_amount=ko.observable(0.0);if(data['register_sales_amount']){self.register_sales_amount(rnum(parseFloat(data['register_sales_amount'])));}
self.register_sales_tax=ko.observable(0.0);if(data['register_sales_tax']){self.register_sales_tax(rnum(parseFloat(data['register_sales_tax'])));}
$.ajax({url:'/ledger/accounts/'+self.date+'.json',dataType:'json',async:false,success:function(data){self.accounts=data;},error:function(){console.log('An error accured on ajax of ledger/accounts.json')}});$.ajax({url:'/inventory/items/'+self.date+'.json',dataType:'json',async:false,success:function(data){self.inventory_items=data;}});self.account_by_name=function(name){var account=$.grep(self.accounts,function(i){return i.name==name;});return account[0];}
self.lotto_sales_dispenser_tax=ko.observable(rnum(parseFloat(self.account_by_name('Lotto Sales').tax_rate)*empty_to_zero(self.lotto_sales_dispenser_amount())/100));self.lotto_sales_register_tax=function(){return rnum(parseFloat(self.account_by_name('Lotto Sales').tax_rate)*rnum(parseFloat(self.lotto_sales_register_amount()))/100);}
self.scratch_off_sales_register_tax=function(){return rnum(parseFloat(self.account_by_name('Scratch Off Sales').tax_rate)*rnum(parseFloat(self.scratch_off_sales_register_amount()))/100);}
self.scratch_off_total=function(){if(isAN(self.lotto_detail.scratch_off_sales_manual()))
return parseFloat(self.lotto_detail.scratch_off_sales_manual());else
return rnum(self.lotto_detail.get_total('sales'));}
self.actual_sales_amount=function(){var total_scratch=self.scratch_off_total();if(total_scratch==0&&self.scratch_off_sales_register_amount()){total_scratch=empty_to_zero(self.scratch_off_sales_register_amount());}
var result=rnum(parseFloat(empty_to_zero(self.cash_sales.get_total('amount')))+parseFloat(empty_to_zero(self.lotto_sales_dispenser_amount()))+parseFloat(empty_to_zero(total_scratch))+parseFloat(empty_to_zero(self.summary_transfer.total())));return result;}
self.actual_sales_tax=function(){var scratch_off_tax=self.scratch_off_sales_dispenser_tax();if(scratch_off_tax==0){scratch_off_tax=self.scratch_off_sales_register_tax();}
var result=rnum(self.cash_sales.get_total('tax')+empty_to_zero(self.lotto_sales_dispenser_tax())+scratch_off_tax);return result;}
self.sales_summary_cash=function(){return rnum(self.actual_sales_amount()-empty_to_zero(self.card_sales.rows()[0].amount())-self.cash_equivalent_sales.get_total('amount'));}
self.diff_sales_amount=function(){return rnum(self.actual_sales_amount()-self.register_sales_amount());}
self.diff_sales_tax=function(){return rnum(self.actual_sales_tax()-self.register_sales_tax());}
self.lotto_changed=function(row){var selected_account=$.grep(self.accounts,function(i){return i.id==row.particular();})[0];if(typeof selected_account=='undefined')
return;$.each(self.cash_sales.rows(),function(key,value){if(value.account_id()==selected_account.id){row.disp(value.amount());return false;}});}
self.account_changed=function(row,event){var selected_account=$.grep(self.accounts,function(i){return i.id==row.account_id();})[0];if(typeof selected_account=='undefined')
return;if(typeof row.tax_rate=='function')
row.tax_rate(selected_account.tax_rate);if(typeof row.additional_tax_rate=='function')
row.additional_tax_rate(selected_account.additional_tax_rate);if(typeof row.opening=='function')
row.opening(selected_account.opening);}
self.account_cr_changed=function(row,event){var selected_account=$.grep(self.accounts,function(i){return i.id==row.account_cr_id();})[0];if(typeof selected_account=='undefined')
return;if(typeof row.tax_rate=='function')
row.tax_rate(selected_account.tax_rate);if(typeof row.additional_tax_rate=='function')
row.additional_tax_rate(selected_account.additional_tax_rate);if(typeof row.opening=='function')
row.opening(selected_account.opening);}
self.inventory_item_changed=function(row){var selected_item=$.grep(self.inventory_items,function(i){return i.id==row.item_id();})[0];if(typeof selected_item=='undefined')
return;row.opening(selected_item.current_stock);}
self.accounts_by_category=function(categories,is_or){var filtered_accounts=[];for(var i in self.accounts){var account_categories=self.accounts[i].categories;if(typeof categories==='string'){if($.inArray(categories,account_categories)!==-1){filtered_accounts.push(self.accounts[i]);}}else if(typeof is_or!='undefined'){if(intersection(categories,account_categories).length){filtered_accounts.push(self.accounts[i]);}}else{if(compare_arrays(categories,account_categories)){filtered_accounts.push(self.accounts[i]);}}}
return filtered_accounts;};self.accounts_by_category_list=function(categories,is_or){var filtered_accounts=[];for(var i=0;i<categories.length;i++){var acc=self.accounts_by_category(categories[i],is_or);for(var j=0;j<acc.length;j++){filtered_accounts.push(acc[j]);}}
return filtered_accounts;};function remove_item(list,item){while(list.indexOf(item)>=0){list.splice(list.indexOf(item),1);}
return list;}
self.accounts_except_category_list=function(categories,is_or){var temp_accounts=deepcopy(self.accounts);for(var i=0;i<categories.length;i++){var acc=self.accounts_by_category(categories[i],is_or);for(var j=0;j<acc.length;j++){temp_accounts=remove_item(temp_accounts,acc[j]);}}
return temp_accounts;};self.accounts_except_category=function(categories,is_or){var filtered_accounts=[];for(var i in self.accounts){var account_categories=self.accounts[i].categories
if(typeof categories==='string'){if($.inArray(categories,account_categories)==-1){filtered_accounts.push(self.accounts[i]);}}else if(typeof is_or!='undefined'){if(!intersection(categories,account_categories).length){filtered_accounts.push(self.accounts[i]);}}else{if(!compare_arrays(categories,account_categories)){filtered_accounts.push(self.accounts[i]);}}}
return filtered_accounts;};self.sales_sans_lotto=function(){var sales_accounts=self.accounts_by_category('Sales');var accounts=[];for(var i in sales_accounts){if(sales_accounts[i].name!='Lotto Sales'&&sales_accounts[i].name!='Scratch Off Sales')
accounts.push(sales_accounts[i]);}
for(var i=0;i<accounts.length;i++){for(var j=0;j<accounts.length-1;j++){if(accounts[j]['name']>accounts[j+1]['name']){var temp=accounts[j];accounts[j]=accounts[j+1];accounts[j+1]=temp;}}}
return accounts;}
self.lotto_sales_dispenser_amount.subscribe(function(){var tax_rate=parseFloat(self.account_by_name('Lotto Sales').tax_rate);self.lotto_sales_dispenser_tax(rnum(parseFloat(self.lotto_sales_dispenser_amount())*tax_rate/100));})
self.scratch_off_sales_dispenser_tax=function(){return rnum(self.scratch_off_total()*self.account_by_name('Scratch Off Sales').tax_rate/100);}
self.inventory_items_by_category=function(category){var filtered_items=[];for(var i in self.inventory_items){if(self.inventory_items[i].category==category)
filtered_items.push(self.inventory_items[i]);}
return filtered_items;}
self.inventory_items_except_category=function(category){var filtered_items=[];for(var i in self.inventory_items){if(self.inventory_items[i].category!=category)
filtered_items.push(self.inventory_items[i]);}
return filtered_items;}
self.account_by_id=function(id){var account=$.grep(self.accounts,function(i){return i.id==id;});if(account.length<1){return self.accounts[0];}
return account[0];}
self.account_for_sales=function(id){var account=$.grep(vm.sales_sans_lotto(),function(i){return i.id==id;});return account[0];}
self.inventory_item_by_id=function(id){var item=$.grep(self.inventory_items,function(i){return i.id==id;});return item[0];}
self.get_unit=function(id){var item=$.grep(self.inventory_items,function(i){return i.id==id;});if(item[0]){return item[0].unit||'';}}
self.save_lotto_sales_as_per_dispenser=function(){self.day_journal_date=self.date;$('#lotto-sales-as-per-dispenser').attr('disabled',true);$.ajax({type:"POST",url:'/day/save_lotto_sales_as_per_dispenser/',data:ko.toJSON(self),success:function(msg){$('#lotto-sales-message').html('Saved!');$('#lotto-sales-message').addClass('success');self.status('Unapproved');},error:function(XMLHttpRequest,textStatus,errorThrown){$('#lotto-sales-message').html('Saving Failed');$('#lotto-sales-message').addClass('error');}});$('#lotto-sales-as-per-dispenser').attr('disabled',false);}
self.save_sales_register=function(){self.day_journal_date=self.date;if(!self.register_sales_amount()){self.register_sales_amount(self.actual_sales_amount());}
if(!self.register_sales_tax()){self.register_sales_tax(self.actual_sales_tax());}
$.ajax({type:"POST",url:'/day/save_sales_register/',data:ko.toJSON(self),success:function(msg){$('#sales-register-message').html('Saved!');$('#sales-register-message').addClass('success');self.status('Unapproved');},error:function(XMLHttpRequest,textStatus,errorThrown){$('#sales-register-message').html('Saving Failed');$('#sales-register-message').addClass('error');}});}
var validate=function(msg,rows,tr_wrapper_id){var selection=$("#"+tr_wrapper_id+" > tr");selection.each(function(index){$(selection[index]).addClass('invalid-row');});for(var i in msg['saved']){rows[i].id=msg['saved'][''+i+''];$(selection[i]).removeClass('invalid-row');}
var model=self[tr_wrapper_id.toUnderscore()];if(typeof(msg.error_message)!='undefined'){model.message(msg.error_message);model.state('error');}
else{var saved_size=Object.size(msg['saved']);if(saved_size==rows.length){model.message('Saved!');self.status('Unapproved');}
else if(saved_size==0){model.message('No rows saved!');model.state('error');}
else if(saved_size<rows.length){var message=saved_size.toString()+' row'+((saved_size==1)?'':'s')+' saved! ';message+=(rows.length-saved_size).toString()+' row'+((rows.length-saved_size==1)?' is':'s are')+' incomplete!';model.message(message);model.state('error');self.status('Unapproved');}}}
var key_to_options=function(key){var dict={rows:data[key],save_to_url:'/day/save/'+key+'/',properties:{day_journal_date:self.date,voucher_no:self.voucher_no},onSaveSuccess:function(msg,rows){validate(msg,rows,key.toDash());}};return dict;}
var cash_sales_options=key_to_options('cash_sales');cash_sales_options.auto_add_first=false;self.cash_sales=new TableViewModel(cash_sales_options,CashSalesRow,"#sales-save");if(self.cash_sales.hasNoRows()){var accounts=self.sales_sans_lotto();for(var i in accounts){self.cash_sales.rows.push(new CashSalesRow({'account_id':accounts[i].id}))}}
var summary_transfer_options=key_to_options('summary_transfer');summary_transfer_options.auto_add_first=false;self.summary_transfer=new TableViewModel(summary_transfer_options,SummaryTransferRow,"#summary-transfer-save");if(self.summary_transfer.hasNoRows()){var accounts=self.accounts_by_category('Transfer and Remittance');for(var i in accounts){self.summary_transfer.rows.push(new SummaryTransferRow({'transfer_type':accounts[i].id}))}}
self.summary_transfer.total=function(){return rnum(self.summary_transfer.get_total('cash'));}
self.summary_transfer.comm_total=function(){return rnum(self.summary_transfer.get_total('commission'));}
self.summary_sales_tax=new TableViewModel(key_to_options('summary_sales_tax'),SummaryTaxRow,'#summary-sales-tax-save');self.summary_sales_tax.rows()[0].register(self.sales_tax);self.summary_inventory=new TableViewModel(key_to_options('summary_inventory'),InventoryRow,'#summary-inventory-save');self.inventory_fuel=new TableViewModel(key_to_options('inventory_fuel'),InventoryRow,'#inventory-fuel-save');self.card_sales=new TableViewModel(key_to_options('card_sales'),CardSalesRow,'#card-sales-save');var cash_equivalent_sales_options=key_to_options('cash_equivalent_sales');cash_equivalent_sales_options.auto_add_first=false;self.cash_equivalent_sales=new TableViewModel(cash_equivalent_sales_options,CashEquivalentSalesRow,'#cash_equivalent_sales-save');if(self.cash_equivalent_sales.hasNoRows()){var accounts=self.accounts_by_category('Cash Equivalent Account');for(var i=0;i<accounts.length;i++){for(var j=0;j<accounts.length-1;j++){if(accounts[j]['name']>accounts[j+1]['name']){var temp=accounts[j];accounts[j]=accounts[j+1];accounts[j+1]=temp;}}}
for(var i in accounts){self.cash_equivalent_sales.rows.push(new CashEquivalentSalesRow({'account':accounts[i].id}))}}
self.summary_cash=new TableViewModel(key_to_options('summary_cash'),SummaryCashRow,'#summary-cash-save');self.summary_cash.rows()[0].actual(rnum(self.cash_actual));var lotto_detail_options=key_to_options('lotto_detail');lotto_detail_options.auto_add_first=false;self.lotto_detail=new TableViewModel(lotto_detail_options,LottoDetailRow,'#lotto_detail-save');if(self.lotto_detail.hasNoRows()){$.ajax({url:'/day/last_lotto_detail/'+self.date+'.json',dataType:'json',async:false,success:function(data){self.last_lotto_detail=data;}});self.last_lotto_detail=self.last_lotto_detail.sort(function(a,b){return a.sn-b.sn;})
if(self.last_lotto_detail){if(Object.size(self.last_lotto_detail)){for(var i in self.last_lotto_detail){var detail=self.last_lotto_detail[i];self.lotto_detail.rows.push(new LottoDetailRow({'rate':detail.rate,'pack_count':detail.pack_count,'day_open':detail.day_open,'day_close':detail.day_close,'addition':detail.addition}))}}
else{self.lotto_detail.addRow(new LottoDetailRow());}}}
self.lotto_detail.scratch_off_sales_manual=ko.observable();if(isAN(data['scratch_off_sales_manual'])){self.lotto_detail.scratch_off_sales_manual(rnum(parseFloat(data['scratch_off_sales_manual'])));}
self.vendor_payout=new TableViewModel(key_to_options('vendor_payout'),VendorPayoutVM,'#vendor-payout-save');self.vendor_charge=new TableViewModel(key_to_options('vendor_charge'),VendorChargeVM,'#vendor-charge-save');self.other_payout=new TableViewModel(key_to_options('other_payout'),OtherPayoutVM,'#other-payout-save');self.deposits=new TableViewModel(key_to_options('deposits'),DepositsVM,'#deposits-save');self.summary_lotto=new SummaryLotto(self);self.approve=function(){var ko_data=JSON.parse(ko.toJSON(self));for(var key in ko_data){if(key!='date')
delete ko_data[key];}
var ko_data=ko.toJSON(ko_data);$.ajax({type:"POST",url:'/day/approve/',data:ko_data,success:function(msg){if(typeof(msg.error_message)!='undefined'){bs_alert.error(msg.error_message);}
else{bs_alert.success('Approved!')
self.status('Approved');self.state('success');if(msg.redirect_to){window.location=msg.redirect_to;}}},error:function(XMLHttpRequest,textStatus,errorThrown){console.log(XMLHttpRequest);}});}}
function LottoDetailRow(row){var self=this;self.rate=ko.observable();self.pack_count=ko.observable();self.day_open=ko.observable();self.day_close=ko.observable();self.addition=ko.observable();self.sales=function(){var day_close=self.day_close();var day_open=self.day_open();if(day_close==0){day_close=1;}
if(day_open==0){day_open=1;}
return rnum((self.addition()+(day_close-day_open))*self.rate());}
for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function CashSalesRow(row){var self=this;self.account_id=ko.observable();self.amount=ko.observable();self.tax=function(){if(self.account_id()){var total=0;if(vm.account_by_id(self.account_id())!='undefined'){total=total+empty_to_zero(self.amount())*empty_to_zero(vm.account_by_id(self.account_id()).sec_tax||0)/100;total=total+empty_to_zero(self.amount())*empty_to_zero(vm.account_by_id(self.account_id()).pri_tax||0)/100;}
return rnum(total);}
return'';}
for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function SummaryTaxRow(row){var self=this;self.register=ko.observable();self.accounts=function(root){var total=0;$.each(root.cash_sales.rows(),function(){if(isAN(this.tax()))
total+=parseFloat(this.tax());});return rnum(total);}
self.difference=function(root){return rnum(self.register()-self.accounts(root));}
for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function InventoryRow(row){var self=this;self.item_id=ko.observable();self.opening=function(){if(self.item_id()){var item_temp=vm.inventory_item_by_id(self.item_id()).get_current_stock;return item_temp;}};self.purchase=ko.observable(0);self.sales=ko.observable(0);self.closing=ko.computed(function(){return rnum(parseFloat(self.opening())+parseFloat(self.purchase())-parseFloat(self.sales()));});self.actual=ko.observable();self.difference=function(){return rnum(self.actual()-self.closing());};for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function SummaryTransferRow(row){var self=this;self.transfer_type=ko.observable();self.cash=ko.observable();self.cheque=ko.observable();self.card=ko.observable();self.commission=ko.observable();for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}
self.valid=function(){if(self.cash()>self.commission()){return true;}
else{return false;}}}
function CardSalesRow(row){var self=this;self.amount=ko.observable();self.commission_out=ko.observable(0);self.net=function(){return rnum(empty_to_zero(self.amount())-empty_to_zero(self.commission_out()));}
for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function CashEquivalentSalesRow(row){var self=this;self.account=ko.observable();self.amount=ko.observable();for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function SummaryCashRow(row){var self=this;self.opening=function(root){var cash_account=root.accounts.filter(function(element,index,array){if(element.name=='Cash Account')
return element;})[0];return rnum(cash_account.opening);};self.inward=function(root){var total=0;total+=parseFloat(root.register_sales_amount());total+=parseFloat(root.register_sales_tax());if(root.card_sales.rows()[0].amount()){total-=parseFloat(root.card_sales.rows()[0].amount());}
total-=root.cash_equivalent_sales.get_total('amount');return rnum(total);};self.outward=function(root){var total=0;$.each(root.vendor_payout.rows(),function(){if(isAN(this.amount())&&this.paid()){var account=root.account_by_id(this.paid());for(var i in account.categories){var category=account.categories[i];if(category=='Cash Account'){total+=parseFloat(this.amount());}}}});$.each(root.other_payout.rows(),function(){if(isAN(this.amount())&&this.paid()){var account=root.account_by_id(this.paid());for(var i in account.categories){var category=account.categories[i];if(category=='Cash Account'){total+=parseFloat(this.amount());}}}});$.each(root.deposits.rows(),function(){if(isAN(this.amount())&&this.deposit_from()){var account=root.account_by_id(this.deposit_from());for(var i in account.categories){var category=account.categories[i];if(category=='Cash Account'){total+=parseFloat(this.amount());}}}});return rnum(total);};self.closing=function(root){return rnum(self.opening(root)+self.inward(root)-self.outward(root));};self.actual=ko.observable();self.difference=function(root){return empty_to_zero(rnum(self.actual()-self.closing(root)));};for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function SummaryLotto(root){var self=this;self.disp=function(){var total=0;$.each(root.lotto_detail.rows(),function(){if(isAN(this.sales()))
total+=this.sales();});return total;}
self.reg=function(){var total=0;$.each(root.cash_sales.rows(),function(){if(typeof this.account_id()!='undefined'){if(root.account_by_id(this.account_id()).name=='Lotto Sales'){total+=this.amount();}}});return total;}
self.diff=function(){return rnum(self.disp()-self.reg());};}
function VendorPayoutVM(row){var self=this;self.vendor=ko.observable();self.amount=ko.observable();self.purchase_ledger=ko.observable();self.remarks=ko.observable();self.paid=ko.observable();self.type=ko.observable();self.types=[{name:'New Purchase',id:'new'},{name:'On Account Payment',id:'old'}];for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function VendorChargeVM(row){var self=this;self.vendor=ko.observable();self.amount=ko.observable();self.purchase_ledger=ko.observable();self.remarks=ko.observable();for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function OtherPayoutVM(row){var self=this;self.paid_to=ko.observable();self.amount=ko.observable();self.remarks=ko.observable();self.paid=ko.observable();for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function DepositsVM(row){var self=this;self.deposit_in=ko.observable();self.amount=ko.observable();self.deposit_from=ko.observable();self.remarks=ko.observable();for(var k in row){if(row[k]!=null)
self[k]=ko.observable(row[k]);}}
function deepcopy(obj){if(Object.prototype.toString.call(obj)==='[object Array]'){var out=[],i=0,len=obj.length;for(;i<len;i++){out[i]=arguments.callee(obj[i]);}
return out;}
if(typeof obj==='object'){var out={},i;for(i in obj){out[i]=arguments.callee(obj[i]);}
return out;}
return obj;}