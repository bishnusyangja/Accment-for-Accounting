$(document).ready(function () {
    $(document).on("click", ".date-picker", function () {
        $(this).datepicker('show');
    });
});


function ChequeReceiptViewModel(data) {
    var self = this;

    self.particulars = new TableViewModel({rows: data.rows}, ChequeReceiptRow);

    for (var k in data)
        self[k] = ko.observable(data[k]);
    self.attachment = ko.observable();

    self.grand_total = function () {
        var total = 0;
        $.each(self.particulars.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
        return rnum(total);
    }





    self.approve = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/bank/cheque-deposit/approve/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                    self.state('error');
                }
                else {
//                        bs_alert.success('Approved!');
                    bs_alert.success('Approved!');
//                        self.state('success');
                    self.status('Approved');
                    if (msg.id){
                        self.id(msg.id);
                        }
                    if (msg.redirect_to){
                        //sconsole.log("entered redirect");
                        window.location = msg.redirect_to;
                        return;
                        }
                }
            }
        });
    }


}

function ChequeReceiptRow(row) {

    var self = this;
    //default values
    self.cheque_number = ko.observable();
    self.cheque_date = ko.observable();
    self.drawee_bank = ko.observable();
    self.drawee_bank_address = ko.observable();
    self.amount = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
}


function ElectronicFundReceiptViewModel(data) {
    var self = this;

    self.particulars = new TableViewModel({rows: data.rows}, ElectronicFundPurchaseRow);


    for (var k in data)
        self[k] = ko.observable(data[k]);
    self.attachment = ko.observable();

    self.grand_total = function () {
        var total = 0;
        $.each(self.particulars.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
        return rnum(total);
    }

    self.approve = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/bank/eft-in/approve/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                    self.state('error');
                }
                else {
//                        bs_alert.success('Approved!');
                    bs_alert.success('Approved!');
//                        self.state('success');
                    self.status('Approved');
                    if (msg.id){
                        self.id(msg.id);
                        }
                    if(msg.redirect_to){
                        window.location = msg.redirect_to;
                        return;
                    }
                }
            }
        });
    }


}

function ElectronicFundPurchaseRow(row) {

    var self = this;
    //default values
    self.transaction_number = ko.observable();
    self.transaction_date = ko.observable();
    self.drawee_bank = ko.observable();
    self.drawee_bank_address = ko.observable();
    self.amount = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
}
