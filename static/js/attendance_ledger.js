// when the document is ready this block of code is executed
$(document).ready(function(){
    $('.selection').select2({
        'placeholder': 'Select Attendance Type'
    });

    vm = new AttendanceVM();
    ko.applyBindings(vm);
    var monthNames = [ "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december" ];
    var objDate = new Date();
    window.month = monthNames[objDate.getMonth()];
    $('.month-tab').click(function(){
        var id = $(this).attr('id').split('-')[0];
        window.month = id;
        ajax_request(id, vm.employee);

    });

    $("#input1").click(function(){
        $("#sele").click(function(){
            $("select.sel").select2();
            var id = monthNames[objDate.getMonth()]
            window.month = id;
            var el = "#"+id+"-tab";
            $(el).parent().attr('class', 'active');
            ajax_request(id, vm.employee);
        });
    });

    $("#sele").click(function(){
        $("#input1").click(function(){
            $("select.sel").select2();
            var id = monthNames[objDate.getMonth()]
            window.month = id;
            var el = "#"+id+"-tab";
            $(el).parent().attr('class', 'active');
            ajax_request(id, vm.employee);
        });
    });

});


function attendance_parameter(obj){
    $.ajax({
        url: '/payroll/attendance-parameter.json',
        dataType: 'json',
        async: false,
        success: function(data){
            obj.parameter = data[0];
        }
    });
}

function employee_ajax(obj){
    $.ajax({
        url: '/payroll/employees.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            obj.employees = data;
        }
    });
}

//attendance view model
function AttendanceVM(){
    var self = this;
    employee_ajax(self);
    attendance_parameter(self);

    self.month = ko.observable();
    self.days = ko.observableArray();
    self.employee = ko.observable();
    self.attendance_type = ko.observable();
    self.hour_attendance = ko.observableArray();
    self.day_attendance = ko.observableArray();


    self.total_time = ko.computed(function(){
        var sum = 0;
        for(var i=0; i < self.hour_attendance().length; i++){
            if(self.hour_attendance()[i].working_time()){
                sum += get_minutes(self.hour_attendance()[i].working_time());
            }
        }
        return get_hrm(sum);
    });

    self.total_day = ko.computed(function(){
        var sum = 0.00;
        for(var i=0; i < self.day_attendance().length; i++){
            var att_status = self.day_attendance()[i].attendance_status();
            if(att_status){
                if(att_status == 'Full Attendance'){
                    sum += self.parameter.full_att;
                }else if(att_status == 'Late Attendance'){
                    sum += self.parameter.late_att;
                }else if(att_status == 'Half Attendance'){
                    sum += self.parameter.half_att;
                }else if(att_status == 'Early Leave'){
                    sum += self.parameter.early_leave;
                }else if(att_status == 'Absent'){
                    sum += self.parameter.abs;
                }

            }
        }

        sum = (Math.round(sum*100)/100).toString() + ' Days';
        return sum;
    });

    self.hour_attendance_status = ko.computed(function(){
        if (this.attendance_type() == 'hour_attendance') return true;
    }, this);
     self.day_attendance_status = ko.computed(function(){
        if (this.attendance_type() == 'day_attendance') return true;
    }, this);

    self.if_changed = function(){
        ajax_request(window.month, self.employee);
    }

    self.up_down = function(){
        arrow_handling();
    }

    self.save = function(){
        $.ajax({
            type: "POST",
            url: '/payroll/save_attendance_ledger/',
            dataType: 'json',
            data: ko.toJSON(self),
            success: function(msg){
                if (typeof (msg.error_message) != 'undefined') {
                        $('#message').html(msg.error_message);
                    }
                else {
                    bs_alert.success('Saved!');
                    return;
                }
            },
            error: function(){
                console.log('An error occurred !');
            }

        });
    }

}


// hour attendance view model
function HourAttendanceVM(data){
    var self = this;

    self.date = ko.observable();
    self.in_time1 = ko.observable();
    self.out_time1 = ko.observable();
    self.in_time2 = ko.observable();
    self.out_time2 = ko.observable();

    if(data){
        self.date(data.date);
        if(data.in_time1){
            self.in_time1 = ko.observable(data.in_time1);
            self.out_time1 = ko.observable(data.out_time1);
        }

        if(data.in_time2){
            self.in_time2 = ko.observable(data.in_time2);
            self.out_time2 = ko.observable(data.out_time2);
        }
    }


    self.working_time = ko.computed(function(){
        if(self.in_time1() && self.out_time1() && self.in_time2() && self.out_time2()){
            return get_hrm(subtract_2_time(self.in_time1(), self.out_time1()) + subtract_2_time(self.in_time2(), self.out_time2()));
        }
        else if(self.in_time1() && self.out_time1()){
            return get_hrm(subtract_2_time(self.in_time1(), self.out_time1()));
        }
        else if(self.in_time2() && self.out_time2()){
            return get_hrm(subtract_2_time(self.in_time2(), self.out_time2()));
        }
        else
            return ;

    },this);

    self.delete_hour = function(){
        $.ajax({
            type: 'GET',
            url: '/payroll/delete-hour-attendance',
            dataType: 'html',
            data: {'date': self.date, 'employee': vm.employee, 'csrfmiddlewaretoken': '{{csrf_token}}'}
        });

        self.in_time1('')
        self.out_time1('')
        self.in_time2('')
        self.out_time2('')

    }

}



// day attendance view model
function DayAttendanceVM(data){
    var self = this;

    self.date = ko.observable();
    self.attendance_status = ko.observable();
    if(data){
        self.date(data.date);
        if(data.attendance_status){
            self.attendance_status(data.attendance_status);
        }
        else{
            self.attendance_status(null);
        }
    }
    self.delete_day = function(){
        $.ajax({
            type: 'GET',
            url: '/payroll/delete-day-attendance/',
            dataType: 'html',
            data: {'date': self.date, 'employee': vm.employee, 'csrfmiddlewaretoken': '{{csrf_token}}'}
        });

        ajax_request(window.month, vm.employee());
        //self.attendance_status(null);

    }
}


//calculation of days for a month
function days_calculation(month){
    month = get_month_index(month);
    var day =  new Date((new Date()).getFullYear(), month+1, 0).getDate();
    var days = new Array();

    for (var i = 1; i <= day; i++)
        days.push(i);

    days.push(month);
    return days;
}


// to get the month index from month name in js started from o index
function get_month_index(month){
    var months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
    for(var i = 0; i<12; i++)
        if (months[i] == month) return i;
}


//formatting date into month/date/year form
function date_format(month, d){
    var date =  new Date();
    var result =  make_2_digit(month+1) + '/' + make_2_digit(d) + '/' + date.getFullYear().toString();
    return result;
}


//converting a single digit number into two digit number and it is used in formatting the date in month and date
function make_2_digit(num){
    var s_num = num.toString()
    if (s_num.length == 1)
        return '0' + s_num;
    else
        return num.toString();
}


// making day_attendance and hour_attendance objects for the given date and employee
function make_day_rows(vm, data){
    //making rows for attendance hour and attendance day
    vm.hour_attendance.removeAll();
    vm.day_attendance.removeAll();
    var index = 0;
    for (var i = 1; i <= vm.days.length; i++){
        if(index < data.length && vm.days[i-1] == data[index].date.split('/')[1]){
            vm.hour_attendance.push(new HourAttendanceVM(data[index]));
            vm.day_attendance.push(new DayAttendanceVM(data[index]));
            index++;
        }
        else{
            var obj_h = new HourAttendanceVM();
            obj_h.date = date_format(vm.month, i);
            vm.hour_attendance.push(obj_h);

            var obj_d = new DayAttendanceVM();
            obj_d.date = date_format(vm.month, i);
            vm.day_attendance.push(obj_d);
        }
    }
}


// for displaying the rows for the given month where the month name is passed by month and the vm is the object of AttendanceVM()
function display_day_rows(vm, month, data){
    var days = days_calculation(month);
    vm.month = days[days.length-1];
    days.pop();
    vm.days = days;
    make_day_rows(vm, data);
    arrow_handling();
    $("select.sel").select2();
}


// creating a javascript object
function create_object(item){
    var obj = new Object();
    obj.name = item;
    return obj;
}


//ajax request when the month-tab is clicked
function ajax_request(month, employee){
    $.ajax({
        type: "POST",
        url: '/payroll/attendance-ledger/',
        dataType: 'html',
        data: {'month': month, 'employee': employee},
        success: function(data){
            data = $.parseJSON(data);
            display_day_rows(vm, month, data);
        },
        error: function(){
            console.log('An error occurred!');
        }

    });
}


// subtracts the two times and returns time period between them
function subtract_2_time(a, b){
    var result = get_minutes(b) - get_minutes(a)
    return result >= 0 ? result : 1440+result;
}


// returns the minutes of the given time
function get_minutes(time){
    var regex = /(\d{1,2})[:|.](\d{1,2})\s*([am|pm|AM|PM|Am|Pm|aM|pM]*)/gi;
    time.replace(regex,  function(_, hour, minute, meridian){
        h = parseInt(hour);
        m = parseInt(minute);
        if(h == 12 && meridian == 'AM'){
            meridian = 'PM'
        }
        else if(h == 12 && meridian == 'PM'){
            meridian = 'AM'
        }
        else{
            meridian = meridian;
        }
        if(meridian == 'PM'){
            time =  720 + h*60 + m;
        }
        if(meridian == 'AM' || meridian == ''){
            time =  h*60 + m;
        }
    });
    return time;
}


// returns the formatted period of the time
function get_hrm(minutes){
    var h = parseInt(minutes/60);
    var m = minutes % 60;
    return make_2_digit(h) + ':' + make_2_digit(m);
}

