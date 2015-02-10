function draw_income_expense(data){

        $('#income_expense_chart').highcharts({
            chart: {
                type: 'column',
                backgroundColor:"#f5f5f5",
                       
            },
            title: {
                align:'center',
                text: 'Income Expense Chart',
                style:{
                        fontSize:'15px',
                }
            },

            yAxis: {
                min: 0,
                title: {
                    text: 'Amount'
                }
            },
            plotOptions: {
                series: {
               // groupPadding:0.1 , 
                pointPadding: 0.01,
                borderWidth: 1, 
                shadow: false
            }
            },
            series: [{
                name: 'Income',
                data: [data['income']]
    
            }, {
                name: 'Expense',
                data: [data['expense']]
    
            }
            ]
        });
    

}



