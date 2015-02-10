$(document).ready(function () {
    $('#phy-date').datepicker({ 'endDate': '0d' }).data('datepicker');
    vm = new PhysicalStockViewModel(ko_data);
    ko.applyBindings(vm);
});

function PhysicalStockViewModel(data) {
    var self = this;

    $.ajax({
        url: '/inventory/items/json/',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = data;
        }
    });

    self.items = self.items.sort(function(a, b) { return compareStrings(a.name, b.name); })
    self.description = ko.observable();
    self.voucher_no = ko.observable();
    self.date = ko.observable();

    for (var k in data)
        self[k] = data[k];

    self.message = ko.observable('');
    self.state = ko.observable('standby');

    self.status = ko.observable(data['status']);

    self.id = ko.observable(data['id']);

    var physical_stock_options = {
        rows: data.particulars
    };

    self.particulars = new TableViewModel(physical_stock_options, ParticularViewModel);

    self.total_amount = function () {
        var sum = 0;
        self.particulars.rows().forEach(function (i) {
            sum += i.amount();
        });
        return rnum(sum);
    }

    self.itemChanged = function (row) {
        var selected_item = $.grep(self.items, function (i) {
            return i.id == row.item_id();
        })[0];
        if (!selected_item) return;
        if (!row.description())
            row.description(selected_item.description);

    }

    self.validate = function () {
        bs_alert.clear();
        var items_list = [];
        for (each in self.particulars.rows()){
            if (items_list.indexOf(self.particulars.rows()[Number(each)].item_id()) == -1)
                items_list.push(self.particulars.rows()[Number(each)].item_id());
            else{
                bs_alert.error('At least one of the items is in multiple rows. Please make sure no item is repeated.');
                return false;
            }
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
            $.ajax({
                type: "POST",
                url: '/inventory/physicalstock/save/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                    }
                    else {
                        bs_alert.success('Saved!');
                        if (msg.id) {
                            self.id(msg.id);
                            self.status('Unapproved');
                        }
                        self.state('success');
                        if (msg.redirect_to) {
                            window.location = msg.redirect_to;
                            return;
                        }
                        $("#particulars-body > tr").each(function (i) {
                            $($("#particulars-body > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows) {
                            self.particulars.rows()[i].id = msg.rows[i];
                            $($("#particulars-body > tr")[i]).removeClass('invalid-row');
                        }

                    }
                }
            });
        }
        else
            return true;
    }

    self.approve = function () {
        if (!self.validate())
            return false;
        //if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/inventory/physicalstock/approve/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                    }
                    else {
                        bs_alert.success('Approved!')
                        self.status('Approved');
                        self.state('success');
                        if (msg.id){
                        self.id(msg.id);
                        }
                        if (msg.redirect_to){

                        window.location = msg.redirect_to;
                        return;
                        }
                    }
                }
            });
        //}
        //else
            //return true;
    }

    self.cancel = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/physicalstock/cancel/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Cancelled!');
                    self.status('Cancelled');
                    self.state('success');
                    if (msg.id)
                        self.id(msg.id);
                }
            }
        });
    }

    self.save_and_continue = function (item, event) {
        if (!self.validate())
            return false;
        if (get_form(event).checkValidity()) {
            $.ajax({
                type: "POST",
                url: '/inventory/physicalstock/save_and_continue/',
                data: ko.toJSON(self),
                success: function (msg) {
                    if (typeof (msg.error_message) != 'undefined') {
                        bs_alert.error(msg.error_message);
                    }
                    else {
                        bs_alert.success('Saved!');
                        if (msg.id)
                            self.id(msg.id);
                        $("#particulars-body > tr").each(function (i) {
                            $($("#particulars-body > tr")[i]).addClass('invalid-row');
                        });
                        for (var i in msg.rows) {
                            self.particulars.rows()[i].id = msg.rows[i];
                            $($("#particulars-body > tr")[i]).removeClass('invalid-row');
                        }
                    }
                }
            });
        }
        else
            return true;
    }

}



function ParticularViewModel(particular) {

    var self = this;
    //default values
    self.item_id = ko.observable();
    self.description = ko.observable();
    self.rate = ko.observable(0);
    self.quantity = ko.observable(1);

    for (var k in particular)
        self[k] = ko.observable(particular[k]);

    
    self.amount = ko.computed(function () {
        var amt = self.quantity() * self.rate();

        return amt;
    });

}

function compareStrings(a, b) {
      if (typeof a == 'undefined') a = '';
      if (typeof b == 'undefined') b = '';
      a = a.toLowerCase();
      b = b.toLowerCase();

      return (a < b) ? -1 : (a > b) ? 1 : 0;
}