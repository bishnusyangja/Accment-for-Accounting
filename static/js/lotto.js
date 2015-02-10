function LottoDetailModel(data){
    var self = this;

    for (var k in data)
        self[k]=data[k];

    $.ajax({
        url: '/inventory/accounts/'+self.date+'.json',
        dataType: 'json',
        async: false,
        success: function(data) {
            self.inventory_accounts = data;
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

    self.inventory_account_changed = function(row){
        var selected_account = $.grep(self.inventory_accounts, function(i){
            return i.id == row.type();
        })[0];
        if (typeof selected_account == 'undefined')
            return;
        if (!row.opening())
            row.opening(selected_account.opening);
        if (!row.rate())
            row.rate(selected_account.rate);
    }

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
            rows: data['lotto_details'],
            save_to_url : '/day/save/lotto_detail/',
            properties : {day_journal_date : self.date},
            onSaveSuccess : function(msg, rows){
                validate(msg, rows, key.toDash());
            }
        };
    }

    self.lotto_detail = new TableViewModel(key_to_options('lotto_detail'), LottoDetailRow);

}



function LottoDetailRow(row){
    var self = this;

    self.type = ko.observable();
    self.rate = ko.observable();
    self.opening = ko.observable();
    self.purchase_pack = ko.observable();
    self.purchase_quantity = ko.observable();
    self.actual_quantity = ko.observable();
    self.sold_quantity = ko.observable();

    self.purchase_total = function(){
        return rnum(self.purchase_pack() * self.purchase_quantity());
    }
    self.purchase_amount = function(){
        return rnum(self.purchase_total() * self.rate());
    }
    self.total = function(){
        return rnum(self.purchase_total() + self.opening());
    }
    self.sold_amount = function(){
        return rnum(self.sold_quantity() * self.rate());
    }
    self.closing_quantity = function(){
        return rnum(self.total() - self.sold_quantity());
    }
    self.closing_amount = function(){
        return rnum(self.closing_quantity() * self.rate());
    }
    self.actual_amount = function(){
        return rnum(self.actual_quantity() * self.rate());
    }
    self.difference_quantity = function(){
        return rnum(self.closing_quantity() * self.actual_quantity());
    }
    self.difference_amount = function(){
        return rnum(self.difference_quantity() * self.rate());
    }

    for (var k in row){
        self[k] = ko.observable(row[k]);
    }
}