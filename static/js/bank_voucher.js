function BankVoucher(data) {
    var self = this;

    for (var k in data)
        self[k] = data[k];

    $.ajax({
        url: '/ledger/accounts.json/',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = data;
        }
    });

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

    var bank_validate = function (msg, rows, tr_wrapper_id, i) {
        var selection = $('#' + tr_wrapper_id + '-' + i + ' > tr');
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']) {
            rows[i].id = msg['saved']['' + i + ''];
            $(selection[i]).removeClass('invalid-row');
        }
        var model = self[tr_wrapper_id.toUnderscore()]()[i];
        var saved_size = Object.size(msg['saved']);
        if (saved_size == rows.length)
            model.message('Saved!');
        else if (saved_size == 0) {
            model.message('No rows saved!');
            model.state('error');
        }
        else if (saved_size < rows.length) {
            var message = saved_size.toString() + ' row' + ((saved_size == 1) ? '' : 's') + ' saved! ';
            message += (rows.length - saved_size).toString() + ' row' + ((rows.length - saved_size == 1) ? ' is' : 's are') + ' incomplete!';
            model.message(message);
            model.state('error');
        }
    }

    //adding new bank accounts if they don't already exist for the current day journal
    for (var i in self.accounts_by_category('Bank')) {
        var account = self.accounts_by_category('Bank')[i];
        var exists = false;
        for (var j in self.bank_detail) {
            var detail = self.bank_detail[j];
            if (detail.bank_account == account.id) {
                exists = true;
            }
        }
        if (!exists) {
            self.bank_detail.push({bank_account: account.id, rows: []});
        }
    }

//    self.summary_bank = new TableViewModel(bank_key_to_option('summary_bank'), BankRow);

    var i = 0;
    self.bank_detail = ko.observableArray(ko.utils.arrayMap(self.bank_detail, function (item) {
        var options = bank_key_to_option(i++);
        return new TableViewModel(options, BankDetailRow);
    }));


    function bank_key_to_option(i) {
        return {
            rows: data.bank_detail[i].rows,
            save_to_url: '/day/save/bank_detail/' + self.bank_detail[i].bank_account + '/',
            properties: {
                day_journal_date: self.date,
                title: self.account_by_id(self.bank_detail[i].bank_account).name,
                bank_account_id: self.bank_detail[i].bank_account,
                id: self.bank_detail[i].id
            },
            onSaveSuccess: function (msg, rows) {
                bank_validate(msg, rows, 'bank-detail', i);
            }
        };
    }


}

function BankDetailRow(row) {

    var self = this;

    self.account_id = ko.observable();
    self.type = ko.observable();
    self.amount = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

}

function BankRow(row) {
    var self = this;

    self.bank_account = ko.observable();
    self.cheque_deposit = ko.observable();
    self.cash_deposit = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
}
