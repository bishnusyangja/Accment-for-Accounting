

function TrialBalance(data) {

    var self = this;

    self.root_nodes = [];

    self.categories = ko.observableArray(ko.utils.arrayMap(data.categories, function (item) {
        self.root_nodes.push(item.id);
        return new CategoryViewModel(item);
    }));

    self.option_show_zero_balance_ledger = ko.observable(false);

    self.option_net_view = ko.observable(true);
    self.option_transactions_view = ko.observable(true);
    self.option_opening_view = ko.observable(true);


    self.expandRoot = function () {
        $('.tree-table').treetable('collapseAll');
        for (var k in self.root_nodes) {
            $('.tree-table').treetable('expandNode', self.root_nodes[k]);
        }
    };
    
    self.opening_dr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.net_opening_dr()))
                total += this.net_opening_dr();
        });
        return total;
    };

    self.opening_cr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.net_opening_cr()))
                total += this.net_opening_cr();
        });
        return total;
    };

    self.transaction_dr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.transaction_dr()))
                total += this.transaction_dr();
        });
        return total;
    };

    self.transaction_cr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.transaction_cr()))
                total += this.transaction_cr();
        });
        return total;
    };


    self.net_transaction_dr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.net_transaction_dr()))
                total += this.net_transaction_dr();
        });
        return total;
    };

    self.net_transaction_cr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.net_transaction_cr()))
                total += this.net_transaction_cr();
        });
        return total;
    };
    
    self.dr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.net_dr()))
                total += this.net_dr();
        });
        return total;
    };

    self.cr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.net_cr()))
                total += this.net_cr();
        });
        return total;
    };

    self.balanced = function () {
        return self.cr_total() == self.dr_total();
    };

    //self.toggleEmpty = function(){
    //    $('.empty').css('display','table-row !important');
    //}
//    self.cls = 'pull-right';

}

function CategoryViewModel(data, parent_id) {

    var self = this;

    self.id = data.id;
    self.name = data.name;
    self.parent_id = parent_id;

    self.accounts = ko.observableArray(ko.utils.arrayMap(data.accounts, function (item) {
        return new AccountViewModel(item, self.id);
    }));

    self.categories = ko.observableArray(ko.utils.arrayMap(data.children, function (item) {
        return new CategoryViewModel(item, self.id);
    }));

    
    self.opening_dr = function () {
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.opening_dr()))
                total += this.opening_dr();
        });
        $.each(self.categories(), function () {
            if (isAN(this.opening_dr()))
                total += this.opening_dr();
        });
        return total;
    }

    self.opening_cr = function () {
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.opening_cr()))
                total += this.opening_cr();
        });
        $.each(self.categories(), function () {
            if (isAN(this.opening_cr()))
                total += this.opening_cr();
        });
        return total;
    }

    self.net_opening_cr = function() {
        if (self.opening_cr() > self.opening_dr())
            return self.opening_cr() - self.opening_dr();
        else
            return 0;
    }

    self.net_opening_dr = function() {
        if (self.opening_dr() >= self.opening_cr())
            return self.opening_dr() - self.opening_cr();
        else
            return 0;
    }
    
    self.closing_dr = function () {
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.closing_dr()))
                total += this.closing_dr();
        });
        $.each(self.categories(), function () {
            if (isAN(this.closing_dr()))
                total += this.closing_dr();
        });
        return total;
    }

    self.closing_cr = function () {
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.closing_cr()))
                total += this.closing_cr();
        });
        $.each(self.categories(), function () {
            if (isAN(this.closing_cr()))
                total += this.closing_cr();
        });
        return total;
    }
    
    
    self.transaction_dr = function () {
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.transaction_dr()))
                total += this.transaction_dr();
        });
        $.each(self.categories(), function () {
            if (isAN(this.transaction_dr()))
                total += this.transaction_dr();
        });
        return total;
    }

    self.transaction_cr = function () {
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.transaction_cr()))
                total += this.transaction_cr();
        });
        $.each(self.categories(), function () {
            if (isAN(this.transaction_cr()))
                total += this.transaction_cr();
        });
        return total;
    }

    self.net_dr = function () {
        if (self.closing_dr() > self.closing_cr())
            return self.closing_dr() - self.closing_cr();
        return 0;
    }

    self.net_cr = function () {
        if (self.closing_cr() > self.closing_dr())
            return self.closing_cr() - self.closing_dr();
        return 0;
    }

    self.net_transaction_dr = function () {
        if (self.transaction_dr() > self.transaction_cr())
            return self.transaction_dr() - self.transaction_cr();
        return 0;
    }

    self.net_transaction_cr = function () {
        if (self.transaction_cr() > self.transaction_dr())
            return self.transaction_cr() - self.transaction_dr();
        return 0;
    }

      self.cls = 'category';


}

function AccountViewModel(data, parent_id) {
    var self = this;
    self.id = data.id;
    self.name = data.name;
    self.parent_id = parent_id;

    self.opening_credit = ko.observable(data.opening_cr);
    self.opening_debit = ko.observable(data.opening_dr);
    self.closing_credit = ko.observable(data.closing_cr);
    self.closing_debit = ko.observable(data.closing_dr);
    self.transaction_credit = ko.observable(data.transaction_cr);
    self.transaction_debit = ko.observable(data.transaction_dr);

    self.opening_cr = function() {
        if(isAN(self.opening_credit()))
            return parseFloat(self.opening_credit());
        else
            return 0;
    }

    self.opening_dr = function() {
        if(isAN(self.opening_debit()))
            return parseFloat(self.opening_debit());
        else
            return 0;
    }

    self.closing_cr = function() {
        if(isAN(self.closing_credit()))
            return parseFloat(self.closing_credit());
        else
            return 0;
    }

    self.closing_dr = function() {
        if(isAN(self.closing_debit()))
            return parseFloat(self.closing_debit());
        else
            return 0;
    }

    self.transaction_cr = function() {
        if(isAN(self.transaction_credit()))
            return parseFloat(self.transaction_credit());
        else
            return 0;
    }

    self.transaction_dr = function() {
        if(isAN(self.transaction_debit()))
            return parseFloat(self.transaction_debit());
        else
            return 0;
    }


    self.net_opening_cr = function() {
        if (self.opening_cr() > self.opening_dr())
            return self.opening_cr() - self.opening_dr();
        else
            return 0;
    }

    self.net_opening_dr = function() {
        if (self.opening_dr() >= self.opening_cr())
            return self.opening_dr() - self.opening_cr();
        else
            return 0;
    }
    

    self.net_dr = function () {
        if (self.closing_dr() >= self.closing_cr()){
            return self.closing_dr() - self.closing_cr();
        }
        return 0;
    }

    self.net_cr = function () {
        if (self.closing_cr() > self.closing_dr()){
            return self.closing_cr() - self.closing_dr();
        }
        return 0;
    }

    self.net_transaction_dr = function () {
        if (self.transaction_dr() >= self.transaction_cr()){
            return self.closing_dr() - self.closing_cr();
        }
        return 0;
    }

    self.net_transaction_cr = function () {
        if (self.transaction_cr() > self.transaction_dr()){
            return self.transaction_cr() - self.transaction_dr();
        }
        return 0;
    }

    self.isVisible = function () {
        return false;
    }


    if ((self.net_cr() == '' || self.net_cr() == null || self.net_cr == '0' ) && (self.net_dr() == '' || self.net_dr() == null || self.net_dr == '0' )) {
        //self.cls = 'account';
        self.cls = 'category';
    } else {
        self.cls = 'category';
    }

}
