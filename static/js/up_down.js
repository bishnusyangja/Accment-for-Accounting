
//Dayjournal data table
var datas = {'#transfer-table':2,'#cash-sales-table':1,'#lotto-sales-table':1,'#actual-sales-table':2,
'#sales-through-cards-table':2,'#sales-through-others-table':1,'#vendor-payout-table':2,
'#other-payout-table':2,'#vendor-charge-table':2,'#deposit-table':2,
'#lotto-fixed-header':5, '#fuel-table': 3,'#other-inventory-table':3,
'#journal-voucher-table':3, '#bank-deposit-table': 3, '#bank-payment-table': 3, '#cash-receipt-table': 3,
'#cash-payment-table': 3, '#physical-stock-voucher-table':3, '#work-time-voucher-table':6,
'#group-payroll-table':5, '#asset-code-table':9, '#asset-ledger-table':2,'#hour-attendance-table':6, "#scratch-off-latest-table":4
}

var locn = null;
function arrow_handling(){
	$('input[target="inside_td"]').bind("keyup", function(event){
	    var index = $("input[target='inside_td']").index(event.target);
	    //var l = find_l();
	    a = "#"+$(this).parent('td').parent('tr').parent('tbody').parent('table').attr('id');
	    locn =datas[a];
	    switch(event.keyCode){
	    	case 37://left arrow
	            index--;
	            if (index < 0) break;
	            $("input[target='inside_td']")[index].focus();
	            break;

	        case 39://right arrow
	            index++;
	            $("input[target='inside_td']")[index].focus();
	            break;

	        case 38://up arrow
	        	for(var i=0; i<locn; i++)
	            	index--;
	            if (index < 0) break;
	            $("input[target='inside_td']")[index].focus();
	            break;

	        case 40: //down arrow
	        	for(var i=0; i<locn; i++)
	            	index++;
	            $("input[target='inside_td']")[index].focus();
	            break;
	    }
	    event.preventDefault();
	});
}
arrow_handling();
