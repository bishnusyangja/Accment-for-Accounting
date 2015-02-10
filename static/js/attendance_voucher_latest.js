// when the document is ready this block of code is executed
$(document).ready(function(){
    $('.selection').select2();

    vm = new AttendanceVM();
    ko.applyBindings(vm);
    display_day_rows(vm, 'january');

    $('.month-tab').click(function(){
        var id = $(this).attr('id').split('-')[0];
        ajax_request(id);
        display_day_rows(vm, id);
    });

});


//attendance view model
function AttendanceVM(){
    var self = this;

    $.ajax({
        url: '/payroll/employees.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.employees = data;
        }
    });

    self.month = ko.observable('january');
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


    self.hour_attendance_status = ko.computed(function(){
        if (this.attendance_type() == 'hour_attendance') return true;
    }, this);
     self.day_attendance_status = ko.computed(function(){
        if (this.attendance_type() == 'day_attendance') return true;
    }, this);


}


// hour attendance view model
function HourAttendanceVM(){
    var self = this;

    self.date = ko.observable();
    self.in_time1 = ko.observable();
    self.out_time1 = ko.observable();
    self.in_time2 = ko.observable();
    self.out_time2 = ko.observable();

    self.working_time = ko.computed(function(){
        if(!self.in_time1() || !self.out_time1() || !self.in_time2() || !self.out_time2()) return;
        return get_hrm(subtract_2_time(self.in_time1(), self.out_time1()) + subtract_2_time(self.in_time2(), self.out_time2()));

    },this);
}



// day attendance view model
function DayAttendanceVM(){
    self = this;

    self.date = ko.observable();
    //self.statuses = [create_object('Full Attendance'), create_object('Late Attendance'), create_object('Half Attendance'), create_object('Early Leave'), create_object('Absent')]
    self.status = ko.observable();

    self.paid = ko.observable('Unpaid');

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


function make_day_rows(vm){
    if (vm.hour_attendance_status){
        vm.hour_attendance.removeAll();
        for (var i = 1; i <= vm.days.length; i++){
            var obj = new HourAttendanceVM();
            obj.date = date_format(vm.month, i);
            vm.hour_attendance.push(obj);
        }
    }

    if (vm.day_attendance_status){
        vm.day_attendance.removeAll();
        for (var i = 1; i <= vm.days.length; i++){
            var obj = new DayAttendanceVM();
            obj.date = date_format(vm.month, i);
            vm.day_attendance.push(obj);
        }
    }

}



// for displaying the rows for the given month where the month name is passed by month and the vm is the object of AttendanceVM()
function display_day_rows(vm, month){
    var days = days_calculation(month);
    vm.month = days[days.length-1];
    days.pop();
    vm.days = days;
    make_day_rows(vm);
}


// creating a javascript object
function create_object(item){
    var obj = new Object();
    obj.name = item;
    return obj;
}


//ajax request when the month-tab is clicked
function ajax_request(month){
    $.ajax({
        url: '/payroll/a/',
        dataType: 'html',
        data: {'month': month},
        success: function(data){
            window.data;
        },
        error: function(){
            console.log('An error occurred!');
        }

    });
}


// subtracts the two times and returns time period between them
function subtract_2_time(a, b){
    var result = remove_am_pm(b) - remove_am_pm(a)
    return result >= 0 ? result : 1440+result;
}


// remove am pm from the time and get 24 hour time value
function remove_am_pm(value){
    var my_string = value.toString();
    my_string = my_string.toUpperCase();
    if(my_string.indexOf('PM') >= 0){
        var value = my_string.split(' ')[0];
        return 720 + get_minutes(value);
    }
    else if(my_string.indexOf('AM') >= 0){
        var value = my_string.split(' ')[0];
        return get_minutes(value);
    }
    else
        return;
}


// returns the minutes of the given time
function get_minutes(tt){
    var hr_m = tt.split(':');
    var h = parseInt(hr_m[0]);
    var m = parseInt(hr_m[1]);
    return h*60 + m;
}


// returns the formatted period of the time
function get_hrm(minutes){
    var h = parseInt(minutes/60);
    var m = minutes % 60;
    return make_2_digit(h) + ':' + make_2_digit(m);
}

