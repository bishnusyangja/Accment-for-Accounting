function draw_income_expense_drilldown_chart(data){

var mon_name_inc = data['mon_name_inc'].reverse();
var mon_name_exp = data['mon_name_exp'].reverse();
var mon_data_inc = data['mon_inc'].reverse();
var mon_data_exp = data['mon_exp'].reverse();  
var tog_inc = [] , tog_exp = [];
for(var i =0;i<mon_data_inc.length;i++){
    var temp1 = [] , temp2 = [];
    temp1.push(mon_name_inc[i]);
    temp1.push(mon_data_inc[i]);
    tog_inc.push(temp1);
    temp2.push(mon_name_exp[i]);
    temp2.push(mon_data_exp[i]);
    tog_exp.push(temp2);
}
//console.log(tog_inc , tog_exp);
$('#income_expense_drilldown_chart').highcharts({
chart:{
            backgroundColor:'#f5f5f5',
            type:'column'
    },    
    title: {
        text: 'Income Expense drilldown'
    },

    xAxis: {
        categories: true
    },
    
    drilldown: {
        series: [
        {
            id: 'income',
            name: 'Income',
            data: tog_inc
        },
        {
            id: 'expense',
            name: 'Expense',
            data:tog_exp
        }]
    },
    
    legend: {
        enabled: false
    },
    
    plotOptions: {
        series: {
            pointPadding:0.01,
            dataLabels: {
                enabled: true
            },
            shadow: false
        }
    },
    
    series: [{
        name: 'Value',
        colorByPoint: true,
        data: [{
            name: 'Income',
            y: data['tot_inc'],
            drilldown: 'income'
        }, {
            name: 'Expense',
            y: data['tot_exp'],
            drilldown: 'expense'
        }]
    }]


});


 }



