$(".customtreetable").treetable({initialState:'expanded',clickableNodeNames:true,expandable:true});$(document).ready(function(){$("div#breadcrumbs div.pull-right").hide();$.ajax({url:'/user/sales-pie-chart/',type:'GET',dataType:'json',success:function(data){$('#sales_chart').removeClass("loading");if(data.sales_accounts!==0){new draw_sales_distribution(data.sales_accounts,5);}}});$.ajax({url:'/user/sales-line-chart/',type:'GET',dataType:'json',success:function(data){$('#sales_distribution_chart').removeClass("loading");if(data.mon_name_sales!==0){new draw_sales_chart(data.monthly_sum_sales,data.mon_name_sales);}}});$.ajax({url:'/user/income-expense-chart/',type:'GET',dataType:'json',success:function(data){$('#income_expense_drilldown_chart').removeClass("loading");if(data.mon_name_income!==0){new draw_income_expense_drilldown_chart({tot_inc:data.income_amount,tot_exp:data.expenses_amount,mon_inc:data.monthly_sum_income,mon_exp:data.monthly_sum_expenses,mon_name_inc:data.mon_name_income,mon_name_exp:data.mon_name_expenses});}}});});function date_calculator(id,difference){var a=new Date();var b=a.getTime();var c=difference*24*60*60*1000;var res=b-c;a.setTime(res);var month=(a.getMonth()+1).toString().length==1?'0'+(a.getMonth()+1):a.getMonth()+1;var date=a.getDate().toString().length==1?'0'+a.getDate():a.getDate();var yesterday=a.getFullYear()+'-'+month+'-'+date;$(id).attr('href','/day/'+yesterday);$(id).attr('tabindex',-1);$(id).html("For "+yesterday);}
date_calculator("#yester",1);date_calculator("#yester2",2);