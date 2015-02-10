function draw_sales_chart(ssum, nname){
    var summ = ssum.reverse();
    var name = nname.reverse();
    // for(var i =0; i<nname.length; i++){
    //     summ.push(ssum[nname.length-i-1]);
    //     name.push(nname[nname.length-i-1]);

    // }

$('#sales_chart').highcharts({
            chart: {
            backgroundColor:"#f5f5f5",

            },
            title: {
                text: 'Sales Chart',
            },
            xAxis: {
                categories: name
            },
            yAxis: {
                title: {
                    text: 'Amount'
                },
                min:0,
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#ff8078'
                }]
            },

            legend: {
                layout: 'vertical',
                align: 'bottom',
                verticalAlign: 'bottom',
                x:100,
                y:0,
                borderWidth: 0
            },
            series: [{
                name: 'Sales',
                data: summ
            }]
        });


}

