$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker({
        endDate:'0d'
        });
    });
    vm = new IndividualPayrollVoucherVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function IndividualPayrollVoucherVM(data) {
    var self = this;
    self.valid = ko.observable(true);
    $.ajax({
        url: '/payroll/employees.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.employees = data;
        }
    });

//    $.ajax({
//        url: '/ledger/payheads.json',
//        dataType: 'json',
//        async: false,
//        success: function (data) {
//            self.payheads = data;
//        }
//    });

    $.ajax({
        url: '/ledger/accounts.json',
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
    self.employee = ko.observable();

    self.days_worked = ko.observable();
    self.hours_worked = ko.observable();
    self.ot_hours_worked = ko.observable();

    self.day_rate = ko.observable();
    self.hour_rate = ko.observable();
    self.ot_hour_rate = ko.observable();

    self.from_date = ko.observable();
    self.to_date = ko.observable();

    for (var k in data) {
    if (data[k])
        self[k] = ko.observable(data[k]);
    }



    self.employee_changed = function (data) {

        if(approved == 1) return;
        var selected_item = $.grep(self.employees, function (i) {
            return i.id == data.employee();
        })[0];
        if (!selected_item) return;

        if (!self.to_date() || !self.employee())
            return;

        $.ajax({
            type: "POST",
            url: '/payroll/employee-detail/',
            dataType: 'html',
            data: {'employee': selected_item.id, 'end': self.to_date},
            success: function(data){
                data = $.parseJSON(data);
                self.hours_worked(data.worked_hours);
                self.days_worked(data.worked_days);
                self.from_date(data.start);
            }


        });

    }

    self.day_amount = function () {
        var value = self.days_worked() * self.day_rate();
        value = isNaN(value)?0:value;
        return value;
    }

    self.hour_amount = function () {
        var value = (self.hours_worked() * self.hour_rate());
        value = isNaN(value)?0:value;
        return value;
    }


    self.total = function () {
        var value = (self.day_amount()) + (self.hour_amount());
        value = isNaN(value)?0:value;
        return value;

    }

    self.accounts_by_category = function (categories, is_or) {
        var filtered_accounts = [];
        for (var i in self.accounts) {
            var account_categories = self.accounts[i].categories
            if (typeof categories === 'string') {
                if ($.inArray(categories, account_categories) !== -1) {
                    filtered_accounts.push(self.accounts[i]);
                }
            } else if (typeof is_or != 'undefined') {
                if (intersection(categories, account_categories).length) {
                    filtered_accounts.push(self.accounts[i]);
                }
            } else {
                if (compare_arrays(categories, account_categories)) {
                    filtered_accounts.push(self.accounts[i]);
                }
            }
        }
        return filtered_accounts;
    };

    self.inclusions = new TableViewModel({rows: data.inclusions}, IndividualPayrollVoucherRowVM);

    self.deductions = new TableViewModel({rows: data.deductions}, IndividualPayrollVoucherRowVM);

    self.validate = function () {
        bs_alert.clear()
        if (!self.employee()) {
            bs_alert.error('"Employee" is required!')
            self.state('error');
            return false;
        }
        var account_list = [];
        for (each in self.inclusions.rows()){
            if (account_list.indexOf(self.inclusions.rows()[Number(each)].account()) == -1)
                account_list.push(self.inclusions.rows()[Number(each)].account());
            else{
                bs_alert.error('There same ledgers in multiple rows of either deductions or inclusions. Please make sure any ledger is not repeated.');
                return false;
            }
        }
        account_list = [];
        for (each in self.deductions.rows()){
            if (account_list.indexOf(self.deductions.rows()[Number(each)].account()) == -1)
                account_list.push(self.deductions.rows()[Number(each)].account());
            else{
                bs_alert.error('There same ledgers in multiple rows of either deductions or inclusions. Please make sure any ledger is not repeated.');
                return false;
            }
        }
        return true;
    }

    self.check_valid = function(){
        if(self.day_rate() && self.hour_rate() && self.voucher_no() && self.date() && self.employee() && self.to_date()){
            var val = self.inclusions.rows();
            if( val.length > 0){
                for (var i =0; i < val.length; i++){
                    if (!val[i].check_valid()){
                        self.valid(false);
                        break;
                    }
                    else{
                        self.valid(true);
                    }
                }
            }
            else{
                self.valid(true);
            }
            if(self.valid()){
                var val = self.deductions.rows();
                if(val.length > 0){
                    for (var i =0; i < val.length; i++){
                        if (!val[i].check_valid()){
                            self.valid(false);
                            break;
                        }
                        else{
                            self.valid(true);
                        }
                    }
                }
                else{
                    self.valid(true);
                }
            }
        }
        return self.valid();
    }

    self.save = function (item, event) {
        if (!self.validate())
            return false;
        if(!self.check_valid()){
            bs_alert.error("Fields are not allowed to be empty.");
            return false;
        }

        if (get_form(event).checkValidity()) {
            if ($(get_target(event)).data('continue')) {
                self.continue = true;
            }
            var data = ko.toJSON(self);
            $.ajax({
                type: "POST",
                url: '/payroll/individual-voucher/save/',
                data: data,
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                        self.state('error');
                    }
                    else {
                        bs_alert.success('Saved!');
                        self.state('success');
                        if (msg.id) {
                            self.id(msg.id);
                            self.status('Unapproved');
                        }
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                        }
                        $("#table-body-inclusions > tr").each(function (i) {
                            $($("#table-body-inclusions > tr")[i]).addClass('invalid-row');
                        });
                        $("#table-body-deductions > tr").each(function (i) {
                            $($("#table-body-deductions > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows1) {
                            self.inclusions.rows()[i].id = msg.rows1[i];
                            $($("#table-body-inclusions > tr")[i]).removeClass('invalid-row');
                        }
                        for (var i in msg.rows2) {
                            self.deductions.rows()[i].id = msg.rows2[i];
                            $($("#table-body-deductions > tr")[i]).removeClass('invalid-row');
                        }
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                        }else{
                            window.location = '/payroll/individual-voucher/'+ msg.id +'/'
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
                url: '/payroll/individual-voucher/approve/',
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
                url: '/payroll/individual-voucher/unapprove/' + self.id() + '/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                        self.state('error');
                    }
                    else {
                        bs_alert.success('Unpproved!');
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

function IndividualPayrollVoucherRowVM(data){
    var self = this;
    self.account = ko.observable();
    self.amount = ko.observable();

    for(var k in data){
        if(data[k])
            self[k] = ko.observable(data[k]);
    }

    self.check_valid = function(){
        if(self.account() && self.amount()){
            return true;
        }
        else{
            return false;
        }
    }
}



function deepcopy(obj) {
    if (Object.prototype.toString.call(obj) === '[object Array]') {
        var out = [], i = 0, len = obj.length;
        for ( ; i < len; i++ ) {
            out[i] = arguments.callee(obj[i]);
        }
        return out;
    }
    if (typeof obj === 'object') {
        var out = {}, i;
        for ( i in obj ) {
            out[i] = arguments.callee(obj[i]);
        }
        return out;
    }
    return obj;
}


