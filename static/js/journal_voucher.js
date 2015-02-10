$(document).ready(function () {
    $('.date-picker').datepicker().data('datepicker');
    vm = new JournalVoucher(ko_data);
    ko.applyBindings(vm);
});

function JournalVoucher(data) {
    var self = this;

    self.date = '';

    for (var k in data)
        self[k] = data[k];

    self.id = ko.observable(data['id']);
    self.status = ko.observable(data['status']);
    self.attachment = ko.observable();

    $.ajax({
        url: '/ledger/accounts.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = data;
        }
    });

    self.accounts_except_category = function (categories, is_or) {
        var filtered_accounts = [];
        for (var i in self.accounts) {
            var account_categories = self.accounts[i].categories;
            if (typeof categories === 'string') {
                if ($.inArray(categories, account_categories) == -1) {
                    filtered_accounts.push(self.accounts[i]);
                }
            } else if (typeof is_or != 'undefined') {
                if (!intersection(categories, account_categories).length) {
                    filtered_accounts.push(self.accounts[i]);
                }
            } else {
                if (!compare_arrays(categories, account_categories)) {
                    filtered_accounts.push(self.accounts[i]);
                }
            }
        }
        return filtered_accounts;
    };

    var validate = function (msg, rows, tr_wrapper_id) {
        var selection = $("#" + tr_wrapper_id + " > tr");
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']) {
            rows[i].id = msg['saved']['' + i + ''];
            $(selection[i]).removeClass('invalid-row');
        }
        var model = self[tr_wrapper_id.toUnderscore()];
        var saved_size = Object.size(msg['saved']);
        if (saved_size == rows.length)
            model.message('Saved!');
        else if (saved_size == 0) {
            model.message('No rows saved!');
            model.status('error');
        }
        else if (saved_size < rows.length) {
            var message = saved_size.toString() + ' row' + ((saved_size == 1) ? '' : 's') + ' saved! ';
            message += (rows.length - saved_size).toString() + ' row' + ((rows.length - saved_size == 1) ? ' is' : 's are') + ' incomplete!';
            model.message(message);
            model.status('error');
        }
    }

    var key_to_options = function (key) {
        return {
            rows: data['rows'],
            save_to_url: '/voucher/journal/save/',
            properties: {id: self.id},
            onSaveSuccess: function (msg, rows) {
                validate(msg, rows, key.toDash());
            }
        };
    }

    self.journal_voucher = new TableViewModel(key_to_options('journal_voucher'), JournalVoucherRow);

    self.journal_voucher.cr_total = ko.computed(function () {
        var total = 0.00;
        $.each(self.journal_voucher.rows(), function () {
            if (isAN(this.cr_amt())) {
                total += parseFloat(this.cr_amt());
            }
        });
        return rnum(total);
    }, self);


    self.journal_voucher.dr_total = ko.computed(function () {
        var total = 0.00;
        $.each(self.journal_voucher.rows(), function () {
            if (isAN(this.dr_amt()))
                total += parseFloat(this.dr_amt());
        });
        return rnum(total);
    }, self);

    self.add_row = function (element, viewModel) {
        $(element).blur();
        var type;
        var dr_amount;
        var cr_amount;
        var diff = self.journal_voucher.dr_total() - self.journal_voucher.cr_total()
        if (diff > 0) {
            type = 'Cr';
            dr_amount = 0;
            cr_amount = diff;
        } else {
            type = 'Dr';
            cr_amount = 0;
            dr_amount = (-1) * diff;
        }

        if ($(element).closest("tr").is(":nth-last-child(2)") && self.journal_voucher.dr_total() != self.journal_voucher.cr_total())
            self.journal_voucher.rows.push(new JournalVoucherRow({type: type, cr_amount: cr_amount, dr_amount: dr_amount}));
    }

    self.journal_voucher.cr_equals_dr = function () {
        return self.journal_voucher.dr_total() === self.journal_voucher.cr_total();
    }

    self.journal_voucher.total_row_class = function () {
        if (self.journal_voucher.dr_total() === self.journal_voucher.cr_total())
            return 'valid-row';
        return 'invalid-row';
    }

    self.journal_voucher.approve = function () {
        var ko_data = JSON.parse(ko.toJSON(self));
        for(var key in ko_data){
            if (key != 'id')
                delete ko_data[key];
        }
        var ko_data = ko.toJSON(ko_data);
        $.ajax({
            type: "POST",
            url: '/voucher/journal/approve/',
            data: ko_data,
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Approved!');
                    self.status('Approved');
                    self.journal_voucher.state('success');
                    if(msg.redirect_to){
                        window.location = msg.redirect_to;
                    }

                }
            }
        });
    }


    self.journal_voucher.cancel = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/voucher/journal/cancel/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Cancelled!');
                    self.status('Cancelled');
                    self.journal_voucher.state('success');
                    if (msg.id)
                        self.id(msg.id);
                }
            }
        });
    }

    self.journal_voucher.save = function (item, event) {

        var ko_data = JSON.parse(ko.toJSON(self));
        delete ko_data.accounts;
        var ko_data = ko.toJSON(ko_data);

        self.journal_voucher.state('waiting');

        var valid = true;
        var message = '';
        var rows = self.journal_voucher.rows();
        var selection = $("#journal-voucher > tr");

        var formdata = new FormData();
        var file = $('#attachment')[0].files[0];       
        formdata.append('attachment', file);
        formdata.append('data', ko_data);

        if (!self.journal_voucher.cr_equals_dr()) {
            message += 'Total Dr and Cr amounts don\'t tally!      ';
            valid = false;
        }

        for(var i =0; i< self.journal_voucher.rows().length; i++){
            if (!self.journal_voucher.rows()[i].has_particulars()){
                if(message.length==0)
                    message += 'Particular is not allowed to be empty!'
                valid = false;
                break;
            }
        }
        var temp_acc = [];
        for(var i =0; i<self.journal_voucher.rows().length; i++){
            if (self.journal_voucher.rows()[i].has_particulars()){

                if(temp_acc.indexOf(self.journal_voucher.rows()[i].account())>=0){
                valid = false;
                message += 'Duplicated Particulars Not Allowed!'
                break;
                }
                else{
                    temp_acc.push(self.journal_voucher.rows()[i].account());
                }

            }
        }

        if (!valid) {
            self.journal_voucher.state('error');
            bs_alert.error(message);
            return false;
        }
        if (get_form(event).checkValidity()) {
            if ($(get_target(event)).data('continue')) {
                self.continue = true;
                formdata.append('continue', self.continue);
            }


            $.ajax({
                type: "POST",
                url: '/voucher/journal/save/',
                async: false,
                processData:false,
                contentType: false,
                cache: false,
                data: formdata,
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                    }
                    else {
                        bs_alert.success('Saved!');
                        self.deleted_rows = [];
                        self.journal_voucher.state('success');
                        if (msg.id) {
                            self.id(msg.id);
                            self.status('Unapproved');
                        }
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                            return;
                        }
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    bs_alert.error('Saving Failed!');
                    self.journal_voucher.state('error');
                }
            });

        }
        else
            return true;
    }
}

function JournalVoucherRow(row) {
    var self = this;
    var selected = $('#selection :selected').text();
    self.type = ko.observable(selected);
    self.account = ko.observable();
    self.description = ko.observable();
    self.dr_amount = ko.observable();
    self.cr_amount = ko.observable();

    self.id = ko.observable();
    self.is_dr = function () {
        if (self.type() == 'Dr'){
            return true;
        }
        return false;
    }

    self.is_cr = function () {
        if (self.type() == 'Cr'){
            return true
        }
        return false;
    }

    self.dr_amt = function(){
        if (this.is_dr())
            return self.dr_amount();
        return 0.00;
        }


    self.has_particulars = function(){
         if(typeof(self.account()) != 'undefined')
            return true;
         else
            return false;

    }


    self.cr_amt = function(){
        if (this.is_cr())
            return this.cr_amount();
        return 0.00;
        }

    self.type_changed = function (e) {
//        console.log(self.type());
    }

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}
