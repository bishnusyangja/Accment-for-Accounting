$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker({
        endDate:'0d'
        });
    });
    if(scenario == 'Create'){
        $('#group-payroll-table').hide();
        $('.btn').hide();
    }


    vm = new GroupPayrollVoucherVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});


function GroupPayrollVoucherVM(data) {
    var self = this;

    $.ajax({
        url: '/payroll/employees.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.employees = data;
        }
    });

    $.ajax({
        url: '/ledger/payheads.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = data;
        }
    });

    self.id = ko.observable();
    self.message = ko.observable();
    self.state = ko.observable('standby');
    self.voucher_no = ko.observable();
    self.date = ko.observable();
    self.from_date = ko.observable();
    self.to_date = ko.observable();

    self.date_range = function(){
        if(self.from_date() && self.to_date()){
            $('#group-payroll-table').show();
            $('.btn').show();
        }
        else
            return;
    }

    for (var k in data) {
        if (data[k])
            self[k] = ko.observable(data[k]);
    }

    var options = {rows: data.rows}

    self.table_vm = new TableViewModel(options, GroupPayrollVoucherRowVM);

    self.check_valid = function(){
        if(!self.date()){
            bs_alert.error('Date is not allowed to be empty !');
            return false;
        }else if(!self.voucher_no()){
            bs_alert.error('Voucher Number is not allowed to be empty !');
            return false;
        }else if(!self.from_date()){
            bs_alert.error('From Date is not allowed to be empty !');
            return false;
        }else if(!self.to_date()){
            bs_alert.error('To Date is not allowed to be empty !');
            return false;
        }else{
            console.log('');
        }

        len = self.table_vm.rows();
        for(var i=0; i<len.length; i++){
            var temp_count = 0;
            for(var j=0; j<len.length; j++){
                if (len[i].employee()==len[j].employee()){
                    if (temp_count == 1){
                        var emp = $.grep(self.employees, function(e){return e.id == len[i].employee(); })[0];
                        bs_alert.error('Multiple Employees with name ' + emp.name + ' are not allowed !');
                        return false;
                    }
                    temp_count += 1;
                }
            }
            if(!len[i].employee()){
                bs_alert.error('Employee is not allowed to be empty !');
                return false;
            }else if(!len[i].rate_day()){
                bs_alert.error('Day Rate is not allowed to be empty !');
                return false;
            }else if(!len[i].rate_hour()){
                bs_alert.error('Hour Rate is not allowed to be empty !');
                return false;
            }else if(!len[i].pay_head()){
                bs_alert.error('Pay Head is not allowed to be empty !');
                return false;
            }else{
                console.log('');
            }
        }
    return true;
    }

    self.save = function (item, event) {
        if (get_form(event).checkValidity()) {
            if ($(get_target(event)).data('continue')) {
                self.continue = true;
            }
            if(!self.check_valid()){
                //bs_alert.error('Fields are not allowed to be empty except payroll tax.')
                return false;
            }

            var data = ko.toJSON(self);
            $.ajax({
                type: "POST",
                url: '/payroll/group-voucher/save/',
                data: data,
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                        self.state('error');
                    }
                    else {
                        bs_alert.success('Saved!');
                        self.state('success');
                        if (msg.id){
                            self.id(msg.id);
                            self.status('Unapproved');
                        }
                        for (var i in msg.rows) {
                            self.table_vm.rows()[i].id = msg.rows[i];
                        }
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                        }else{
                            window.location = '/payroll/group-voucher/'+ msg.id +'/'
                        }
                    }
                }
            });
        }
        else
            return true;
    }

    self.approve = function (item, event) {
            $.ajax({
                type: "POST",
                url: '/payroll/group-voucher/approve/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                        self.state('error');
                    }
                    else {
                        bs_alert.success('Approved!');
                        self.state('success');
                        self.status('Approved');
                        if (msg.id)
                            self.id(msg.id);
                        window.location = msg.redirect_to;
                    }
                }
            });
    }

    self.unapprove = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/payroll/group-voucher/unapprove/' + self.id() + '/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                    self.state('error');
                }
                else {
                    bs_alert.success('Unapproved!');
                    self.state('success');
                    self.status('Unapproved');
                    if (msg.id)
                        self.id(msg.id);
                    window.location = msg.redirect_to;
                }
            }
        });
    }
}

function GroupPayrollVoucherRowVM(data) {

    var self = this;

    self.employee = ko.observable();
    self.present_days = ko.observable();
    self.present_hours = ko.observable();
    self.present_ot_hours = ko.observable();
    self.rate_day = ko.observable();
    self.rate_hour = ko.observable();
    self.rate_ot_hour = ko.observable();
    self.payroll_tax = ko.observable();
    self.pay_head = ko.observable();

    for (var k in data)
        if (data[k])
            self[k] = ko.observable(data[k]);

    self.employee_changed = function (row) {
        if(approved == 1) return;
        var selected_item = $.grep(vm.employees, function (i) {
            return i.id == row.employee();
        })[0];
        if (!selected_item) return;

        $.ajax({
            type: "POST",
            url: '/payroll/employee-detail/',
            dataType: 'html',
            data: {'employee': selected_item.id, 'start': vm.from_date, 'end': vm.to_date},
            success: function(data){
                data = $.parseJSON(data);
                self.present_hours(data.worked_hours);
                self.present_days(data.worked_days);
            }
        });
    }


    self.amount = ko.computed(function () {
        return (round2z(self.present_days()) * round2z(self.rate_day()) + round2z(self.present_hours()) * round2z(self.rate_hour())).toFixed(2);
    });

    self.net = ko.computed(function () {
        return (self.amount() - round2z(self.payroll_tax())).toFixed(2);
    });

    self.is_valid = function () {
        if (self.net() < 0.0) return false;
        else return true;
    };

    self.style = function () {
        if (self.net() < 0.0) return "invalid-row";
        else return "valid-row";
    };

}

