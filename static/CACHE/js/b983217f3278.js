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
arrow_handling();$(document).ready(function(){$('.selection').select2({'placeholder':"Select Attendance Type"});vm=new AttendanceVM();ko.applyBindings(vm);var monthNames=["january","february","march","april","may","june","july","august","september","october","november","december"];var objDate=new Date();window.month=monthNames[objDate.getMonth()];$('.month-tab').click(function(){var id=$(this).attr('id').split('-')[0];window.month=id;ajax_request(id,vm.employee);});$("#input1").click(function(){$("#sele").click(function(){$("select.sel").select2();var id=monthNames[objDate.getMonth()]
window.month=id;var el="#"+id+"-tab";$(el).parent().attr('class','active');ajax_request(id,vm.employee);});});$("#sele").click(function(){$("#input1").click(function(){$("select.sel").select2();var id=monthNames[objDate.getMonth()]
window.month=id;var el="#"+id+"-tab";$(el).parent().attr('class','active');ajax_request(id,vm.employee);});});});function employee_ajax(obj){$.ajax({url:'/payroll/employees.json',dataType:'json',async:false,success:function(data){obj.employees=data;}});}
function AttendanceVM(){var self=this;employee_ajax(self);self.month=ko.observable();self.days=ko.observableArray();self.employee=ko.observable();self.attendance_type=ko.observable();self.hour_attendance=ko.observableArray();self.day_attendance=ko.observableArray();self.total_time=ko.computed(function(){var sum=0;for(var i=0;i<self.hour_attendance().length;i++){if(self.hour_attendance()[i].working_time()){sum+=get_minutes(self.hour_attendance()[i].working_time());}}
return get_hrm(sum);});self.hour_attendance_status=ko.computed(function(){if(this.attendance_type()=='hour_attendance')return true;},this);self.day_attendance_status=ko.computed(function(){if(this.attendance_type()=='day_attendance')return true;},this);self.if_changed=function(){ajax_request(window.month,self.employee);}
self.up_down=function(){arrow_handling();}
self.save=function(){$.ajax({type:"POST",url:'/payroll/save_attendance_ledger/',dataType:'json',data:ko.toJSON(self),success:function(msg){if(typeof(msg.error_message)!='undefined'){$('#message').html(msg.error_message);}
else{bs_alert.success('Saved!');return;}},error:function(){console.log('An error occurred !');}});}}
function HourAttendanceVM(data){var self=this;self.date=ko.observable();self.in_time1=ko.observable();self.out_time1=ko.observable();self.in_time2=ko.observable();self.out_time2=ko.observable();if(data){self.date(data.date);if(data.in_time1){self.in_time1=ko.observable(data.in_time1);self.out_time1=ko.observable(data.out_time1);}
if(data.in_time2){self.in_time2=ko.observable(data.in_time2);self.out_time2=ko.observable(data.out_time2);}}
self.working_time=ko.computed(function(){if(self.in_time1()&&self.out_time1()&&self.in_time2()&&self.out_time2()){return get_hrm(subtract_2_time(self.in_time1(),self.out_time1())+subtract_2_time(self.in_time2(),self.out_time2()));}
else if(self.in_time1()&&self.out_time1()){return get_hrm(subtract_2_time(self.in_time1(),self.out_time1()));}
else if(self.in_time2()&&self.out_time2()){return get_hrm(subtract_2_time(self.in_time2(),self.out_time2()));}
else
return;},this);self.delete_hour=function(){$.ajax({type:'GET',url:'/payroll/delete-hour-attendance',dataType:'html',data:{'date':self.date,'employee':vm.employee,'csrfmiddlewaretoken':'{{csrf_token}}'}});self.in_time1('')
self.out_time1('')
self.in_time2('')
self.out_time2('')}}
function DayAttendanceVM(data){var self=this;self.date=ko.observable();self.attendance_status=ko.observable();if(data){self.date(data.date);if(data.attendance_status){self.attendance_status(data.attendance_status);}
else{self.attendance_status(null);}}
self.delete_day=function(){$.ajax({type:'GET',url:'/payroll/delete-day-attendance/',dataType:'html',data:{'date':self.date,'employee':vm.employee,'csrfmiddlewaretoken':'{{csrf_token}}'}});ajax_request(window.month,vm.employee());}}
function days_calculation(month){month=get_month_index(month);var day=new Date((new Date()).getFullYear(),month+1,0).getDate();var days=new Array();for(var i=1;i<=day;i++)
days.push(i);days.push(month);return days;}
function get_month_index(month){var months=['january','february','march','april','may','june','july','august','september','october','november','december'];for(var i=0;i<12;i++)
if(months[i]==month)return i;}
function date_format(month,d){var date=new Date();var result=make_2_digit(month+1)+'/'+make_2_digit(d)+'/'+date.getFullYear().toString();return result;}
function make_2_digit(num){var s_num=num.toString()
if(s_num.length==1)
return'0'+s_num;else
return num.toString();}
function make_day_rows(vm,data){vm.hour_attendance.removeAll();vm.day_attendance.removeAll();var index=0;for(var i=1;i<=vm.days.length;i++){if(index<data.length&&vm.days[i-1]==data[index].date.split('/')[1]){vm.hour_attendance.push(new HourAttendanceVM(data[index]));vm.day_attendance.push(new DayAttendanceVM(data[index]));index++;}
else{var obj_h=new HourAttendanceVM();obj_h.date=date_format(vm.month,i);vm.hour_attendance.push(obj_h);var obj_d=new DayAttendanceVM();obj_d.date=date_format(vm.month,i);vm.day_attendance.push(obj_d);}}}
function display_day_rows(vm,month,data){var days=days_calculation(month);vm.month=days[days.length-1];days.pop();vm.days=days;make_day_rows(vm,data);arrow_handling();$("select.sel").select2();}
function create_object(item){var obj=new Object();obj.name=item;return obj;}
function ajax_request(month,employee){$.ajax({type:"POST",url:'/payroll/attendance-ledger/',dataType:'html',data:{'month':month,'employee':employee},success:function(data){data=$.parseJSON(data);display_day_rows(vm,month,data);},error:function(){console.log('An error occurred!');}});}
function subtract_2_time(a,b){var result=get_minutes(b)-get_minutes(a)
return result>=0?result:1440+result;}
function get_minutes(time){var regex=/(\d{1,2})[:|.](\d{1,2})\s*([am|pm|AM|PM|Am|Pm|aM|pM]*)/gi;time.replace(regex,function(_,hour,minute,meridian){h=parseInt(hour);m=parseInt(minute);if(h==12&&meridian=='AM'){meridian='PM'}
else if(h==12&&meridian=='PM'){meridian='AM'}
else{meridian=meridian;}
if(meridian=='PM'){time=720+h*60+m;}
if(meridian=='AM'||meridian==''){time=h*60+m;}});return time;}
function get_hrm(minutes){var h=parseInt(minutes/60);var m=minutes%60;return make_2_digit(h)+':'+make_2_digit(m);}