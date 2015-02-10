$(document).ready(function(){$("#selectChoice").select2();hide_sub_form();var category=get_category();request_ajax(category);$("form select[name='category']").on("click",function(){var category=get_category();request_ajax(category);});show_for_update(scenario);});function category_form(check){if(check!==''){var cat_form="#"+check;hide_sub_form();$(cat_form).show();}
if(check=='bank_account'){$("form input[name='bank_address']").geocomplete();}
if(check=='party_account'){$("form input[name='party_address']").geocomplete();}}
function hide_sub_form(){$('#bank_account').hide();$('#party_account').hide();$('#account_tax').hide();}
function request_ajax(category){if(category!=''){$.ajax({url:'/ledger/detect_category/',type:'POST',data:{'category':category},dataType:'html',success:function(result){if(result!==0){category_form(result);}},error:function(){console.log("An error occurred !");}});}}
function show_for_update(scenario){if(scenario=='Update'){var category=get_category();request_ajax(category);}}
function get_category(){var category=$("select[name=category]").val();var required="#id_category option[value="+category+"]";category=$(required).text();var patt=/-*\s*/;category=category.replace(patt,'');return category;}
function has_if(item,checklist){for(var i=0;i<checklist.length;i++){if(item==checklist[i])
return true;}
return false;}
var scenario="Update"
var base="dashboard.html"