function ProfitAndLoss(data) {

    var self = this;

    self.root_nodes = [];

    self.categories = ko.observableArray(ko.utils.arrayMap(data.categories, function (item) {
        self.root_nodes.push(item.id);
        return new CategoryViewModel(item, data.total_revenue);
    }));

    self.option_show_zero_balance_ledger = ko.observable(false);

    self.option_net_view = ko.observable(true);

    self.n_p = ko.observable(data.gross_profit);

    self.net_profit = self.n_p();

    self.net_profit_pct = self.net_profit * 100 / parseFloat(data.total_revenue);

    self.expandRoot = function () {
        $('.tree-table').treetable('collapseAll');
        for (var k in self.root_nodes) {
            $('.tree-table').treetable('expandNode', self.root_nodes[k]);
        }
    };

    //self.toggleEmpty = function(){
    //    $('.empty').css('display','table-row !important');
    //}

}

function CategoryViewModel(data, total_revenue, parent_id) {

    var self = this;

    self.id = data.id;
    self.name = data.name;
    self.parent_id = parent_id;

    self.accounts = ko.observableArray(ko.utils.arrayMap(data.accounts, function (item) {
        return new AccountViewModel(item, total_revenue, self.id);
    }));

    self.categories = ko.observableArray(ko.utils.arrayMap(data.children, function (item) {
        return new CategoryViewModel(item, total_revenue, self.id);
    }));

    self.net_amount = function () {
        var total = 0;
        if (isAN(data.amount))
            return parseFloat(data.amount);
        $.each(self.accounts(), function () {
            if (isAN(this.net_amount()))
                total += this.net_amount();
        });
        $.each(self.categories(), function () {
            if (isAN(this.net_amount()))
                total += this.net_amount();
        });
        return total;

    }


    self.pct_of_revenue = function() {
        var pct = self.net_amount() * 100.00 / parseFloat(total_revenue);
            return pct;

    }
}

function AccountViewModel(data, total_revenue, parent_id) {
    var self = this;
    self.id = data.id;
    self.name = data.name;
    self.parent_id = parent_id;
    self.link = data.link;
    self.transaction_credit = ko.observable(data.transaction_cr);
    self.transaction_debit = ko.observable(data.transaction_dr);

    self.net_amount = function () {
        if (self.transaction_debit() >= self.transaction_credit()){
            return self.transaction_debit() - self.transaction_credit();
        }
        else if (self.transaction_credit() >= self.transaction_debit()){
            return self.transaction_credit() - self.transaction_debit();
        }
        return 0;
    }


    self.isVisible = function () {
        return false;
    }

    self.pct_of_revenue = function() {
        var pct = self.net_amount() * 100.00 / parseFloat(total_revenue);
            return pct;
    }
}

function neg(value){
    value = value.toString();

    if(value[0] == '-'  && value.length > 1){
        value = value.replace('-','');
        value = '(' +value + ')'
        value = value.fontcolor("red");
    }
    else
        value = value;
    return value;
}
