$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new CashReceiptVM(ko_data);
    ko.applyBindings(vm);
});


function CashReceiptVM(data) {
    var self = this;

    $.ajax({
        url: '/ledger/party/customers.json',
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
    self.receipt_on = ko.observable();
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

    //self.party_address(selected.address);
    //self.current_balance(selected.customer_balance);


    var selected_obj = $.grep(self.parties,function(i){
        return i.id == self.party()
    })[0];
    self.party_address(selected_obj.address);
    self.current_balance(selected_obj.customer_balance);

}


function CashReceiptRowVM(row) {
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
