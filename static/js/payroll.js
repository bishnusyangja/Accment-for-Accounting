function PayrollEntryModel(data){
    var self = this;



    $.ajax({
        url: '/ledger/accounts.json',
        dataType: 'json',
        async: false,
        success: function(data) {
            self.accounts = data;
        }
    });

    self.accounts_by_category = function(categories, is_or){
        var filtered_accounts = [];
        for (var i in self.accounts){
            var account_categories = self.accounts[i].categories
            if( typeof categories === 'string' ) {
                if ($.inArray(categories, account_categories) !== -1){
                    filtered_accounts.push(self.accounts[i]);
                }
            }else if(typeof is_or != 'undefined'){
                if (intersection(categories, account_categories).length){
                    filtered_accounts.push(self.accounts[i]);
                }
            }else{
                if (compare_arrays(categories, account_categories)){
                    filtered_accounts.push(self.accounts[i]);
                }
            }
        }
        return filtered_accounts;
    };

    var validate = function(msg, rows, tr_wrapper_id){
        var selection = $("#" + tr_wrapper_id + " > tr");
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']){
            rows[i].id = msg['saved'][''+i+''];
            $(selection[i]).removeClass('invalid-row');
        }
        var model = self[tr_wrapper_id.toUnderscore()];
        var saved_size = Object.size(msg['saved']) ;
        if(saved_size==rows.length)
            model.message('Saved!');
        else if(saved_size==0){
            model.message('No rows saved!');
            model.status('error');
        }
        else if(saved_size<rows.length){
            var message = saved_size.toString() +' row' + ((saved_size==1)?'':'s') + ' saved! ';
            message += (rows.length-saved_size).toString() +' row' + ((rows.length-saved_size==1)?' is':'s are') + ' incomplete!';
            model.message(message);
            model.status('error');
        }
    }

    var key_to_options = function(key){
        return {
            rows: data['rows'],
            save_to_url : '/payroll/save/',
            properties : {id : self.id},
            onSaveSuccess : function(msg, rows){
                self.payroll_entry.id = msg.id;
                validate(msg, rows, key.toDash());
            }
        };
    }

    self.payroll_entry = new TableViewModel(key_to_options('payroll_entry'), PayrollEntryRow);

    self.payroll_entry.entry_no = ko.observable(data.entry_no);

}


function PayrollEntryRow(row){
    var self = this;

    self.account_id = ko.observable();
    self.pay_heading = ko.observable();
    self.amount = ko.observable();
    self.hours = ko.observable();
    self.tax = ko.observable();
    self.remarks = ko.observable();

    for (var k in row){
        self[k] = ko.observable(row[k]);
    }

}
