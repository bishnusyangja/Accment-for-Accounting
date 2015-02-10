$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new CashPaymentVM(ko_data);
    ko.applyBindings(vm);
});


function CashPaymentVM(data) {
    var self = this;

    $.ajax({
        url: '/ledger/party/suppliers.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.parties = data;
        }
    });

    self.id = ko.observable('');
    self.message = ko.observable();
    self.state = ko.observable('standby');
    self.party = ko.observable();
    self.payment_on = ko.observable();
    self.party_address = ko.observable();
    self.reference = ko.observable();
    self.current_balance = ko.observable();
    self.amount = ko.observable();
    self.voucher_no = ko.observable();
    self.table_vm = ko.observable({'rows': function () {
    }, 'get_total': function () {
    }});

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }


    self.party_changed = function (vm) {
        var selected_obj = $.grep(self.parties, function (i) {
            return i.id == vm.party();
        })[0];
        self.party_address(selected_obj.address);
        self.current_balance(selected_obj.supplier_balance);
    }


    self.load_purchase_vouchers = function () {
        if (self.party()) {
            $.ajax({
                url: '/voucher/purchase/party/' + self.party() + '.json',
                dataType: 'json',
                async: false,
                success: function (data) {
                    if (data.length) {
                        self.invoices = data;
                        for (k in self.rows()) {
                            var row = self.rows()[k];
                            $.each(self.invoices, function (i, o) {
                                if (o.id == row.id) {
                                    o.payment = row.payment;
                                    o.discount = row.discount;
                                }
                            });
                        }
                        var options = {
                            rows: self.invoices
                        };
                        self.table_vm(new TableViewModel(options, CashPaymentRowVM));
                        bs_alert.success('Purchase Vouchers loaded!');
                        self.state('success');
                    }
                    else {
                        bs_alert.warning('No pending purchase vouchers found for the supplier!');
                        self.state('error');
                    }
                }
            });
        }

    }

    if (self.rows().length) {
        self.load_purchase_vouchers();
    }

    self.total_payment = ko.computed(function () {
        return self.table_vm().get_total('payment');
    }, self);

    self.total_discount = ko.computed(function () {
        return self.table_vm().get_total('discount');
    }, self);

    self.validate = function () {
        if (!self.party()) {
            bs_alert.error('"Party" field is required!')
            self.state('error');
            return false;
        }
        return true;
    }

    self.save = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            if ($(get_target(event)).data('continue')) {
                self.continue = true;
            }

            var data = ko.toJSON(self);
            $.ajax({
                type: "POST",
                url: '/voucher/cash-payment/save/',
                data: data,
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                        self.state('error');
                    }
                    else {
                        bs_alert.success('Saved!');
                        self.status('Unapproved');
                        self.state('success');
                        if (msg.id)
                            self.id(msg.id);
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                        }
                    }
                }
            });
        }
        else
            return true;
    }

    self.approve = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/voucher/cash-payment/approve/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                        self.state('error');
                    }
                    else {
                        bs_alert.success('Approved!');
                        self.status('Approved');
                        self.state('success');
                        if (msg.id){
                            self.id(msg.id);
                        }
                        if (msg.redirect_to){
                            window.location = msg.redirect_to;
                        }

                    }
                }
            });
        }
        else
            return true;
    }
}


function CashPaymentRowVM(row) {
    var self = this;

    self.payment = ko.observable();
    self.discount = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

    self.overdue_days = function () {
        if (self.due_date()) {
            var diff = days_between(new Date(self.due_date()), new Date());
            if (diff >= 0)
                return diff;
        }
        return '';
    }

}
