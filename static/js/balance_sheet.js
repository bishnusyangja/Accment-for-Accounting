

function BalanceSheet(data) {

    var self = this;

    self.root_nodes = [];

    self.asset_total = 0.0;

    self.categories = ko.observableArray(ko.utils.arrayMap(data.categories, function (item) {
        self.root_nodes.push(item.id);
        return new CategoryViewModel(item);
    }));

    self.expandRoot = function () {
        $('.tree-table').treetable('collapseAll');
        for (var k in self.root_nodes) {
            $('.tree-table').treetable('expandNode', self.root_nodes[k]);
        }
    };

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

    self.amount = function () {
        if (this.name == 'Total Assets' || this.name == 'Total Equity' || this.name == 'Total Equity And Liabilities' || this.name == 'Total Liabilities')
            return data.amt;
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.amount()))
                total += this.amount();
        });
        $.each(self.categories(), function () {
            if (this.name != 'Total Assets' && this.name != 'Total Equity' && this.name != 'Total Equity And Liabilities' && this.name != 'Total Liabilities'){
                if (isAN(this.amount()))
                    total += this.amount();
                }
            });

        return total;
    }

    self.cls = 'category';


}

function AccountViewModel(data, parent_id) {
    var self = this;
    self.id = data.id;
    self.name = data.name;
    self.parent_id = parent_id;

    self.amount = function () {
        if (isAN(data.amount))
            return parseFloat(data.amount);
        else
            return 0;
    }

    self.cls = 'category';
}
