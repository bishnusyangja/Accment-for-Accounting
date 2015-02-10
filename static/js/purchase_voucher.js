$(document).ready(function () {
    //$('#inv-date').datepicker().data('datepicker');
    //$('#due-date').datepicker({relative_to: '#inv-date'});
    $('.date-picker').datepicker();
    vm = new PurchaseVoucherViewModel(ko_data);
    ko.applyBindings(vm);
});

function TaxOptions(name, id) {
    this.name = name;
    this.id = id;
}


function PurchaseVoucherViewModel(data) {
    var self = this;

    self.tax_options = ko.observableArray([
        new TaxOptions('Tax Inclusive', 'inclusive'),
        new TaxOptions('Tax Exclusive', 'exclusive'),
        new TaxOptions('No Tax', 'no')
    ]);

    $.ajax({
        url: '/inventory/items/json/',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = data;
        }
    });

    $.ajax({
        url: '/ledger/party/suppliers.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.suppliers = data;
        }
    });

    $.ajax({
        url: '/tax/schemes/json/',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.tax_schemes = data;
        }
    });

    self.tax_scheme_by_id = function (id) {
        var scheme = $.grep(self.tax_schemes, function (i) {
            return i.id == id;
        });
        return scheme[0];
    }

    $.ajax({
        url: '/ledger/accounts.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = data;
        }
    });

    self.party = ko.observable();
    self.description = ko.observable();

    for (var k in data)
        self[k] = data[k];

    self.tax = ko.observable(data['tax']);
    self.id = ko.observable(data['id']);
    self.status = ko.observable(data['status']);

    self.message = ko.observable('');
    self.state = ko.observable('standby');

    self.party_address = ko.observable('');



    self.accounts_by_category = function (categories, is_or) {
        var filtered_accounts = [];
        for (var i in self.accounts) {
            var account_categories = self.accounts[i].categories;
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


    var options = {
        rows: data.particulars
    };

    self.particulars = new TableViewModel(options, ParticularViewModel);

//    self.addParticular = function() {
//        var new_item_index = self.particulars().length+1;
//        self.particulars.push(new ParticularViewModel({ sn: new_item_index }));
//    };
//
//    self.removeParticular = function(particular) {
//        for (var i = particular.sn(); i < self.particulars().length; i++) {
//            self.particulars()[i].sn(self.particulars()[i].sn()-1);
//        };
//        self.particulars.remove(particular);
//    };

    self.validate = function(){
        var rows = self.particulars.rows();
        if(rows.length == 0){
            bs_alert.error('No rows to save.');
            return false;
        }
        else{
            for(var i = 0; i < rows.length; i++ ){
                if(!rows[i].validate()){
                    return false;
                }
            }
            return true;
        }

    }

    self.save = function (item, event) {
        if(!self.validate()){
            return false;
        }
        var formdata = new FormData();
        var file = $('#id_attachment')[0].files[0];
        formdata.append('data', ko.toJSON(self));
        formdata.append('attachment', file);


        $.ajax({
            type: "POST",
            url: '/voucher/purchase-voucher/save/',
            data: formdata,
            processData: false,
            contentType: false,
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    $('#message').html(msg.error_message);
                }
                else {
                    bs_alert.success('Saved!');
                    //$('#message').html('Saved!');
                    if (msg.id)
                        self.id = msg.id;
                    /* $("#particulars-body > tr").each(function (i) {
                        $($("#particulars-body > tr")[i]).addClass('invalid-row');
                    });
                    for (var i in msg.rows) {
                        self.particulars.rows()[i].id = msg.rows[i];
                        $($("#particulars-body > tr")[i]).removeClass('invalid-row');
                    }*/
                    window.location = '/voucher/purchase-voucher/'+ msg.id;

                }
            },
            error:  console.log('error is occured')
        });
    }

    self.save_continue = function (item, event) {
        if(!self.validate()){
            return false;
        }
        var formdata = new FormData();
        var file = $('#id_attachment')[0].files[0];
        formdata.append('data', ko.toJSON(self));
        formdata.append('attachment', file);


        $.ajax({
            type: "POST",
            url: '/voucher/purchase-voucher/save/',
            data: formdata,
            processData: false,
            contentType: false,
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    $('#message').html(msg.error_message);
                }
                else {
                    bs_alert.success('Saved!');
                    window.location = '/voucher/purchase-voucher/';

                }
            },
            error:  console.log('error is occured')
        });
    }

    self.sub_total = function () {
        var sum = 0;
        self.particulars.rows().forEach(function (i) {
            sum += i.amount();
        });
        return rnum(sum);
    }

    self.tax_amount = function () {
        var sum = 0;
            self.particulars.rows().forEach(function (i) {
                if (typeof self.tax_scheme_by_id(i.tax_scheme()) != 'undefined') {
                    var tax_percent = self.tax_scheme_by_id(i.tax_scheme()).percent;
                    var tax_amount = i.amount() * (tax_percent / 100);
                    sum += tax_amount;
                }

            });

        return rnum(sum);
    }

    self.validate = function () {
        bs_alert.clear();
        if (!self.party) {
            bs_alert.error('"From" field is required!');
            self.state('error');
            return false;
        }
        var rows = self.particulars.rows();
        if (rows.length == 0){
            bs_alert.error('No rows to save.');
        }
        else{
            for(var i=0; i < rows.length; i++){
                if(!rows[i].validate()){
                    return false;
                }
            }
        }
        return true;
    }


    self.itemChanged = function (row) {
        var selected_item = $.grep(self.items, function (i) {
            return i.id == row.item_id();
        })[0];
        if (!selected_item) return;
        if (!row.description())
            row.description(selected_item.description);
//        if (!row.unit_price())
//            row.unit_price(selected_item.sales_price);
        if (!row.tax_scheme())
            row.tax_scheme(selected_item.tax_scheme);
    }

    self.supplier_changed = function (vm) {
        var selected_obj = $.grep(self.suppliers, function (i) {
            return i.id == vm.party;
        })[0];
        self.party_address(selected_obj.address);
    }

    self.particulars.grand_total = ko.computed(function () {
            return self.sub_total() + self.tax_amount();
        return rnum(self.sub_total());
    }, self);

    self.approve = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/voucher/purchase-voucher/approve/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                    }
                    else {
                        bs_alert.success('Approved!')
                        self.status('Approved');
                        self.state('success');
                    }
                    window.location = '/voucher/purchase-voucher/' + self.id();
                }
            });
        }
        else
            return true;
    }

    self.unapprove = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/voucher/purchase-voucher/unapprove/' + self.id() + '/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                    }
                    else {
                        bs_alert.success('Unapproved!')
                        self.status('Unapproved');
                        self.state('success');
                    }
                    window.location = '/voucher/purchase-voucher/' + self.id();
                }
            });
        }
        else
            return true;
    }

//    self.cancel = function (item, event) {
//        $.ajax({
//            type: "POST",
//            url: '/voucher/purchase/cancel/',
//            data: ko.toJSON(self),
//            success: function (msg) {
//                if (typeof (msg.error_message) != 'undefined') {
//                    bs_alert.error(msg.error_message);
//                }
//                else {
//                    bs_alert.success('Cancelled!');
//                    self.status('Cancelled');
//                    self.state('success');
//                    if (msg.id)
//                        self.id = msg.id;
//                }
//            }
//        });
//    }

}

function ParticularViewModel(particular) {

    var self = this;
    //default values
    self.account = ko.observable();
    self.description = ko.observable();
    self.unit_price = ko.observable(0);
    self.quantity = ko.observable(1);
    self.discount = ko.observable(0).extend({ numeric: 2 });
    self.tax_scheme = ko.observable();

    for (var k in particular)
        self[k] = ko.observable(particular[k]);

    if (self.discount() == null)
        self.discount(0);

    self.amount = ko.computed(function () {
        var wo_discount = self.quantity() * self.unit_price();
        var amt = wo_discount - ((self.discount() * wo_discount) / 100);

        return amt;
    });

    self.validate = function(){
        if(!self.account()){
            bs_alert.error('Particular is not allowed to be empty');
            return false;
        }
        else if(!self.unit_price()){
            bs_alert.error('Price is not allowed to be empty.');
            return false;
        }
        else if(!self.quantity()){
            bs_alert.error('Quantity is not allowed to be empty.');
            return false;
        }
        else{
            return true;
        }
    }

}

