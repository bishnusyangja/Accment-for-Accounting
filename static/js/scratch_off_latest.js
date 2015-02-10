$(document).ready(function () {
    $('.date-picker').datepicker({
        endDate:'0d'
    });
    /*
    $(document).on("click", ".date-picker", function () {
        $(this).datepicker({
            endDate: '0d'
        });
    });
    */
});

function ScratchOffLatestViewModel(data) {
    var self = this;
    var temp;
    var date = Date.parseExact(data.date, "MM/dd/yyyy").toString("yyyy-MM-dd");;
    //self.particulars = new TableViewModel({rows: data.rows}, ScratchOffLatestRow);

    if (data.id == null){
        $.ajax({
            type:"GET",
            url:"/day/get-previous-scratch-off/" + date+"/",
            datatype: 'json',
            async:false,
            success : function(data){
                temp = new TableViewModel({rows: data.rows}, ScratchOffLatestRow);
            }

        });
    }
    else {
        temp = new TableViewModel({rows: data.rows}, ScratchOffLatestRow);
    }
    self.particulars = temp;
    for (var k in data){
            self[k] = ko.observable(data[k]);
    }

    self.grand_total = function () {
        var tot = 0;
        $.each(self.particulars.rows(), function () {
            if (isAN(this.total()))
                tot += parseFloat(this.total());
        });
        return rnum(tot);
    }

    self.validate = function(){
        var in_time = $('#id_in_time').val();
        var out_time = $('#id_out_time').val();

        if(!in_time){
            bs_alert.error("In time is required!");
            return false;
        }if(!out_time){
            bs_alert.error("Out time is required!");
            return false;
        }
        if(compare_time(in_time, out_time) != out_time){
            bs_alert.error('In time must be less than out time!');
            return false;
        }

        var temp = self.particulars.rows();
        if(temp.length == 0){
            bs_alert.error("No rows to Save!");
            return false;
        }
        for(var i = 0; i<temp.length; i++){
            if(!temp[i].validate())
                return false;
        }
        return true;
    }

    self.save = function(){
            if(!self.validate()){
                return;
            }
        $.ajax({
            type: "POST",
            url: '/day/scratch-off-latest/save/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Saved!');
                    if (msg.id){
                        self.id(msg.id);
                    }
                    if (msg.redirect_to){

                        window.location = msg.redirect_to;
                        return;
                        }
                }
            }
        });
 }

}

function ScratchOffLatestRow(row) {

    var self = this;
    //default values
    self.rate = ko.observable();
    self.packet_count = ko.observable();
    self.in_count = ko.observable();
    self.out_count = ko.observable();
    self.addition = ko.observable(0);

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

    self.total = ko.computed(function(){
           var day_close = self.out_count();
           var day_open = self.in_count();
           var addition = self.addition();
            if (day_close == 0) {
            day_close = 1;
                }
            if (day_open == 0){
                day_open = 1;
            }
            if(addition == 0){
            addition=0;
            }
            var to = rnum(( parseInt(day_close,10) - parseInt(day_open,10) + parseInt(addition,10)) * self.rate());
            return to;
    }, self);

    self.validate = function(){
        if(!self.rate()){
            bs_alert.error("Rate is Required!");
            return false;
        }
        else if(!self.packet_count()){
            bs_alert.error("Packet Count is Required!");
            return false;
        }
        else if(!self.in_count()){
            bs_alert.error("In Count is Required!");
            return false;
        }
        else if(!self.out_count()){
            bs_alert.error("Out Count is Required!");
            return false;
        }else if(parseInt(self.in_count()) > parseInt(self.packet_count())){
            bs_alert.error('In count is not allowed to be greater than packet count!');
            return false;
        }else if(parseInt(self.out_count()) > parseInt(self.packet_count())){
            bs_alert.error('Out count is not allowed to be greater than packet count!');
            return false;
        }
        else if(!self.addition() && (parseInt(self.in_count()) > parseInt(self.out_count()) || self.in_count() == self.out_count())){
            bs_alert.error('Out count must be greater than in count if no addition!');
            return false;
        }else if(parseInt(self.addition()) < parseInt(self.packet_count())){
            bs_alert.error('Addition must be greater than packet count!');
            return false;
        }
        else{
            return true;
        }
    }
}

function compare_time(a, b){
    var a_list = a.split(' ');
    var b_list = b.split(' ');
    if(a_list[1] == 'PM' && b_list[1] == 'AM'){
        return a;
    }
    else if(a_list[1] == 'AM' && b_list[1] == 'PM'){
        return b;
    }else{
        var res = compare_t(a_list[0], b_list[0]);
        if(res == a_list[0]){
            return a;
        }else if(res == b_list[0]){
            return b;
        }else{
            return '';
        }
    }
}

function compare_t(a, b){
    var a_lis = a.split(':');
    var b_lis = b.split(':');

    var hr_a = hr_12(parseInt(a_lis[0]));
    var min_a = parseInt(a_lis[1]);

    var hr_b = hr_12(parseInt(b_lis[0]));
    var min_b = parseInt(b_lis[1]);

    if (hr_a > hr_b){
        return a;
    }else if (hr_b > hr_a){
        return b;
    }else{
        if(min_a > min_b){
            return a;
        }else if (min_b > min_a){
            return b;
        }else{
            return '';
        }
    }
}

function hr_12(value){
    if(value == 12){
        return 0;
    }
    else{
        return value;
    }
}