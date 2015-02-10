$(document).ready(function () {
    $(document).ready(function () {
        $('.date-picker').datepicker();
    });
    vm = new FixedAssetVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});


function FixedAssetVM(data) {
    var self = this;

    $.ajax({
        url: '/ledger/cash-and-vendors.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.from_accounts = data;
        }
    });

    $.ajax({
        url: '/ledger/fixed-assets.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.fixed_assets = data;
        }
    });

    self.id = ko.observable('');
    self.message = ko.observable();
    self.state = ko.observable('standby');
    self.from_account = ko.observable();
    self.voucher_no = ko.observable();
    self.party_address = ko.observable();
    self.date = ko.observable();
    self.reference = ko.observable();
    self.voucher_no = ko.observable();

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

    var options = {
        rows: data.rows
    };

    self.table_vm = new TableViewModel(options, FixedAssetRowVM);

    var options2 = {
        rows: data.additional_details
    }

    self.additional_details = new TableViewModel(options2, AdditionalDetailVM);

    self.account_changed = function (vm) {
        var selected_obj = $.grep(self.from_accounts, function (i) {
            return i.id == vm.from_account();
        })[0];
        if (selected_obj) {
            self.party_address(selected_obj.address);
        }
    }

    self.validate = function () {
        if (!self.from_account()) {
            bs_alert.error('"From" field is required!')
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
                url: '/voucher/fixed-asset/save/',
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
                            return;
                        }
                        window.location = '/voucher/fixed-asset/'+ self.id();

                        $("#rows-body > tr").each(function (i) {
                            $($("#rows-body > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows1) {
                            self.table_vm.rows()[i].id = msg.rows1[i];
                            $($("#rows-body > tr")[i]).removeClass('invalid-row');
                        }
                        $("#additional-body > tr").each(function (i) {
                            $($("#additional-body > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows2) {
                            self.additional_details.rows()[i].id = msg.rows2[i];
                            $($("#additional-body > tr")[i]).removeClass('invalid-row');
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
                url: '/voucher/fixed-asset/approve/',
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
                        window.location = '/voucher/fixed-asset/'+ self.id();
                    }
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
                url: '/voucher/fixed-asset/unapprove/',
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
                        window.location = '/voucher/fixed-asset/'+ self.id();
                    }
                }
            });
        }
        else
            return true;
    }
}

function FixedAssetRowVM(row) {
    var self = this;

    self.asset_ledger = ko.observable();
    self.description = ko.observable();
    self.amount = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

}

function AdditionalDetailVM(row) {
    var self = this;

    self.assets_code = ko.observable();
    self.assets_type = ko.observable();
    self.vendor_name = ko.observable();
    self.vendor_address = ko.observable();
    self.amount = ko.observable();
    self.useful_life = ko.observable();
    self.description = ko.observable();
    self.warranty_period = ko.observable();
    self.maintenance = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}