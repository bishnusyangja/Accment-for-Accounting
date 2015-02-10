$(document).ready(function(){
    $("#selectChoice").select2();
    hide_sub_form();
    //var base = base;
    var category = get_category();
    request_ajax(category);

    $("form select[name='category']").on("click", function () {
        var category = get_category();
        request_ajax(category);
    });
    show_for_update(scenario);
});


function category_form(check){
    //if one is selected and other forms are removed and selected again the same the form not displayed, so to make that form display
    if(check !== ''){
        var cat_form = "#"+check;
        hide_sub_form();
        $(cat_form).show();
    }
    if(check == 'bank_account'){
        $("form input[name='bank_address']").geocomplete();
    }

    if(check == 'party_account'){
        $("form input[name='party_address']").geocomplete();
    }


}


// hides the bank_account_form, party_account_form and account_tax_detail form
function hide_sub_form(){
    $('#bank_account').hide();
    $('#party_account').hide();
    $('#account_tax').hide();
}


// sends an ajax request to check whether the category needs to display the other sub-form or not.
function request_ajax(category){
    if(category != ''){
        $.ajax({
            url: '/ledger/detect_category/',
            type: 'POST',
            data: {'category': category},
            dataType: 'html',
            success: function(result){
                if(result !== 0){
                    category_form(result);
                }
            },
            error: function(){
                console.log("An error occurred !");
            }
        });
    }
}


// to show the sub-form value in updated form
function show_for_update(scenario){
    if( scenario == 'Update'){
        var category = get_category();
        request_ajax(category);
    }
}


//to get the selected category value from the account_form to check to display the other form or not
function get_category(){
    var category = $("select[name=category]").val();
    var required = "#id_category option[value=" + category + "]";
    category = $(required).text();
    var patt = /-*\s*/;
    category = category.replace(patt, '');
    return category;
}


function has_if(item, checklist){
    for(var i = 0; i < checklist.length; i++ ){
        if(item == checklist[i])
            return true;
    }
    return false;
}
