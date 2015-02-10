function draw_sales_distribution(data , threshold){
    var res = merge_lower_sales(data,threshold);
    Highcharts.setOptions({
    lang: {
        drillUpText: 'Back',

    }
        });
    var options = {
             chart:{
            backgroundColor:'#f5f5f5',
            type:'pie',
            height:250,
    },    
    title: {
        text: 'Sales Distribution Chart'
    },

    xAxis: {
        categories: true
    },
    
    drilldown: {
        series: [
        {
            id: 'others',
            name: 'Others',
            data: res[0]
        }]
    },
    
    legend:{
                itemStyle: {
                cursor: 'pointer',
                color: '#274b6d',
                fontSize: '8.5px'
                },
                align:'right',
                verticalAlign:'top',
                x:-5,
                y:100,
                layout:'vertical'
            },
    
    plotOptions: {
         pie: {
            borderWidth: 1.5,
                borderColor : '#000000',
            },
        series: {

            dataLabels: {
                enabled: false
            },
            shadow: false,
            showInLegend: true
        }
    },
    
    series: [{
        name: 'value',
        colorByPoint: true,
        data: res[1]
    }]
    };
    options.chart.renderTo = 'sales_distribution_chart';
    var chart2 = new Highcharts.Chart(options);
    // var res = merge_lower_sales(data,threshold);
    //     $('#sales_distribution_chart').highcharts({
           

    //     });

}


//merging the sales values according to threshold
function merge_lower_sales(data , threshold){
    var amounts=[] , together = [] , lesser = [] , greater = [];
    for(var i =0;i<data.length;i++){
            var tog = new Object();
            amounts.push(data[i]['cr']);
            
            if(data[i]['name']=='Sales'){
            tog.name = data[i]['name']
            }
            else {
                tog.name = data[i]['name'].replace(/Sales/g,'');
            }
            
            tog.cr = data[i]['cr'];
            together.push(tog);
    }
//get total amount
    var total = function(arr) {
        tot  = 0;
        for(var j = 0; j<arr.length ; j++){
                tot += arr[j];
        }
        return tot;
    };

    var mytot = total(amounts);
    var thres = threshold*mytot/100;    //get threshold amount

var less_tot = 0;
    // naking data format suiting to the highchart 
    for(var i = 0; i<together.length; i++){
        //var less_tot  = 0;
        var temparr = []
        if(together[i]['cr'] < thres){ 
            temparr.push(together[i]['name']);
            temparr.push(together[i]['cr']);
            lesser.push(temparr);
            less_tot += together[i]['cr'];
        }
        else{
            var tempobj = new Object();
            tempobj.name = together[i]['name'];
            tempobj.y = together[i]['cr'];
            greater.push(tempobj);
            }
    }
    greater.push({name:'Others', y:less_tot, drilldown:'others'});


//var tot_tog = total(together['cr']);
//console.log(lesser ,thres , greater)
return [lesser , greater] ;
   
}

// var a = merge_lower_sales(tryone , 10);
// console.log(a[0] , a[1])



