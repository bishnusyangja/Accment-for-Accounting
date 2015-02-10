$(document).ready(function () {
    vm = new WorkTimeVoucherVM(ko_data);
    $('.date-picker').datepicker({
        endDate:'0d'
    });
    ko.applyBindings(vm);
});


function WorkTimeVoucherVM(data) {
    var self = this;
    $.ajax({
        url: '/payroll/employees.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.employees = data;
        }
    });

    self.employee = ko.observable();
    self.id = ko.observable();
    self.message = ko.observable();
    self.state = ko.observable('standby');
    self.voucher_no = ko.observable();
    self.date = ko.observable();
    self.from_date = ko.observable();
    self.to_date = ko.observable();
    self.work_days = ko.observableArray();
    self.has_range = ko.observable();


    if(data){
        for (var k in data) {
            if(data[k] && typeof data[k] == 'object'){
                var the_date = new Date(data.from_date);
                for(var i = 0; i < data[k].length; i++){
                    self.work_days.push(new WorkDayVM(data[k][i], new DateM(the_date)));
                    the_date.setDate(the_date.getDate() + 1);
                }
            }
            else
                self[k] = ko.observable(data[k]);
        }

    }

    self.date_changed = function () {
        self.has_range(false);
        if (!self.from_date() || !self.to_date())
            return;
        self.has_range(true);
        var the_date = new Date(self.from_date());
        while (the_date <= new Date(self.to_date())) {
            var new_date = new DateM(the_date);
            var match = $.grep(self.work_days(), function (i) {
                return i.day_string == new_date.mm_dd_yyyy();
            })[0];

            if (!match) {
               self.work_days.push(new WorkDayVM({}, new_date))

            }
            the_date.setDate(the_date.getDate() + 1);
        }

        if (typeof self.work_days == 'function') {
                self.work_days(self.work_days().sort(function (a, b) {
                    var x = (new Date(a.day.date_string)).getTime();
                    var y = (new Date(b.day.date_string)).getTime();
                    return (x - y);
                }));
        }

        var days_to_remove = [];
        var from = new Date(self.from_date());
        var to = new Date(self.to_date());
        for (var i = 0; i < self.work_days().length; i++) {
            var day = self.work_days()[i];
            var my_date = new Date(day.day_string);
            if (my_date < from || my_date > to) {
                days_to_remove.push(day);
            }
        }
        for (var i = 0; i < days_to_remove.length; i++) {
            self.work_days.remove(days_to_remove[i]);
        }
    }

    self.date_changed();



    self.save = function (item, event) {
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/payroll/attendance-voucher/save/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        $('#message').html(msg.error_message);
                    }
                    else {
                        bs_alert.success('Saved!');
                        window.location = '/payroll/attendance-voucher/' + msg.id + '/';
                        return;
                    }
                }
            });
        }
        else
            return true;
    }

    self.save_continue = function(item, event){
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/payroll/attendance-voucher/save/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        $('#message').html(msg.error_message);
                    }
                    else {
                        bs_alert.success('Saved!');
                        window.location = '/payroll/attendance-voucher/';
                        return;
                    }
                }
            });
        }
        else
            return true;
    }

    self.total_time = function () {
        var total = 0;
        if(self.work_days()[0])
        for (var i = 0; i < self.work_days().length; i++) {

            if (self.work_days()[i].work_time()) {
                var work_time = self.work_days()[i].work_time();
                var hours = parseInt(work_time.split(':')[0]);
                var minutes = parseInt(work_time.split(':')[1]);
                var total_minutes = hours * 60 + minutes;
                total += total_minutes;
            }
        }
        var total_hours = Math.floor(total / 60);
        var total_minutes = total % 60;
        return total_hours + ':' + total_minutes;
    }

}


function WorkDayVM(data, day) {
    var self = this;

    self.in_time1 = ko.observable();
    self.out_time1 = ko.observable();
    self.in_time2 = ko.observable();
    self.out_time2 = ko.observable();

    for (var k in data) {
        if (data[k])
            self[k] = ko.observable(data[k]);
    }

    self.work_time = ko.computed(function () {

        var in_time1_raw = self.in_time1();
        var out_time1_raw = self.out_time1();

        var in_time2_raw = self.in_time2();
        var out_time2_raw = self.out_time2();

        if(!in_time1_raw || !out_time1_raw || !in_time2_raw || !out_time2_raw)
            return;
        var t1 = get_minutes(in_time1_raw);
        var t2 = get_minutes(out_time1_raw);
        var t3 = get_minutes(in_time2_raw);
        var t4 = get_minutes(out_time2_raw);

        var d1 = time_diff(t2, t1);
        var d2 = time_diff(t4, t3);

        var result = d1+d2;
        return get_hr_m(result);

    }, this);
    self.day = day;
    self.day_string = day.mm_dd_yyyy();
}

function DateM(date) {
    var self = this;

    self.date = date;
    self.weekday = get_weekday(date);
    self.date_string = date.toUTCString();
    self.day = date.getDate();
    self.month = date.getMonth() + 1; //Months are zero based
    self.year = date.getFullYear();

    self.mm_dd_yyyy = ko.computed(function () {
        var month = self.month;
        var day = self.day;
        if (month < 10)
            month = '0' + month;
        if (day < 10)
            day = '0' + day;
        return month + '/' + day + '/' + self.year;
    }, this);
}


function get_hr_m(m){
    var hr = parseInt(m/60);
    var min = m % 60;
    return hr + ":" + min;
}


function get_minutes(t){
    var regex = /(\d{1,2}):(\d{1,2})\s*([am|pm|AM|PM|Am|Pm]*)/gi;
    t.replace(regex, function(_, hours, minutes, meridian) {
        h = parseInt(hours);
        m = parseInt(minutes);
        if (meridian.toLowerCase() == 'pm'){
            if(h != 12)
                h += 12;
        }
        if(meridian.toLowerCase() == 'am'){
            if(h == 12)
                h += 12
        }
        if(h == 24){
            h = 0;
        }
        t = h*60 + m;
        });
    return t;
}

function time_diff(a, b){
    res = a-b;
    if(res < 0){
        res += 24*60;
    }
    return res;
}
