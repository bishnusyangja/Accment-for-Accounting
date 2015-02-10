$(document).ready(function () {
    $('.date-picker').datepicker({
            endDate: '0d'
    });

    /*
    $(document).on("click", ".date-picker", function () {
        $(this).datepicker('show');
    });
    */

    $("#clear-attachment").click(function(){
        clearFileInput("id_attachment");
    });
});

function BankDepositViewModel(data) {
    var self = this;

    self.particulars = new TableViewModel({rows: data.rows}, BankDepositRow);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    $.ajax({
        url: '/ledger/accounts.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = data;
        }
    });

    self.attachment = ko.observable();

    self.grand_total = function () {
        var total = 0;
        $.each(self.particulars.rows(), function () {
            if (isAN(this.amount()))
                total += parseFloat(this.amount());
        });
        return rnum(total);
    }

    self.validate = function(){
        var temp = self.particulars.rows();
        if(temp.length == 0){
            bs_alert.error("No rows to Save!");
            return false;
        }
        for(var i = 0; i<temp.length; i++){
            if(!temp[i].validate())
                return false;
        }
        return true;
    }

    self.approve = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/bank/bank-deposit/approve/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                    //self.state('error');
                }
                else {
                    bs_alert.success('Approved!');
                    //self.state('success');
                    self.status('Approved');
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
    }

    self.save = function(){
            if(!self.validate()){
                return;
            }
            var formdata = new FormData();
            var file = $('#id_attachment')[0].files[0];
            formdata.append('data', ko.toJSON(self));
            formdata.append('attachment', file);

        $.ajax({
            type: "POST",
            url: '/bank/bank-deposit/save/',
            data: formdata,
            processData: false,
            contentType: false,
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Saved!');
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
    //var notify = humane.create({ timeout: 10000, baseCls: 'humane-jackedup' })
    //notify.log('Saved!')
 }

    self.save_and_continue = function(){
            var formdata = new FormData();
            var file = $('#id_attachment')[0].files[0];
            formdata.append('data', ko.toJSON(self));
            formdata.append('attachment', file);
        $.ajax({
            type: "POST",
            url: '/bank/bank-deposit/save/',
            data: formdata,
            processData: false,
            contentType: false,
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Saved!');
                    if (msg.id){
                        self.id(msg.id);
                    }
                    window.location = '/bank/bank-deposit/';
                    return;

                }
            }
        });
    }


}

function BankDepositRow(row) {

    var self = this;
    //default values
    self.from_account = ko.observable();
    self.reference_no = ko.observable();
    self.description = ko.observable();
    self.amount = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

    self.validate = function(){
        if(!self.from_account()){
            bs_alert.error("From Field is Required!");
            return false;
        }
        else if(!self.amount()){
            bs_alert.error("Amount Field is Required!");
            return false;
        }
        else{
            return true;
        }
    }
}


function BankPaymentViewModel(data) {
    var self = this;

    self.particulars = new TableViewModel({rows: data.rows}, BankPaymentRow);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    $.ajax({
        url: '/ledger/accounts.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.accounts = data;
        }
    });

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
            url: '/bank/bank-payment/approve/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                    //self.state('error');
                }
                else {
                    bs_alert.success('Approved!');
                    //self.status('Approved');
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
    }

    self.validate = function(){
        var temp = self.particulars.rows();
        if(temp.length == 0){
            bs_alert.error("No rows to Save!");
            return false;
        }
        for(var i = 0; i<temp.length; i++){
            if(!temp[i].validate())
                return false;
        }
        return true;
    }


    self.save = function(){
            if(!self.validate()){
                return;
            }
            var formdata = new FormData();
            var file = $('#id_attachment')[0].files[0];
            formdata.append('data', ko.toJSON(self));
            formdata.append('attachment', file);
        $.ajax({
            type: "POST",
            url: '/bank/bank-payment/save/',
            data: formdata,
            processData: false,
            contentType: false,
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Saved!');
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
    }

    self.save_and_continue = function(){
            var formdata = new FormData();
            var file = $('#id_attachment')[0].files[0];
            formdata.append('data', ko.toJSON(self));
            formdata.append('attachment', file);
        $.ajax({
            type: "POST",
            url: '/bank/bank-payment/save/',
            data: formdata,
            processData: false,
            contentType: false,
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Saved!');
                    if (msg.id){
                        self.id(msg.id);
                    }
                    window.location = '/bank/bank-payment/';
                    return;

                }
            }
        });
    }
}

function BankPaymentRow(row) {

    var self = this;
    //default values
    self.to_account = ko.observable();

    self.reference_no = ko.observable();
    self.description = ko.observable();
    self.amount = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

    self.validate = function(){
        if(!self.to_account()){
            bs_alert.error("To Field is Required!");
            return false;
        }
        else if(!self.amount()){
            bs_alert.error("Amount Field is Required!");
            return false;
        }
        else{
            return true;
        }
    }
}



function clearFileInput(id){
    var oldInput = document.getElementById(id);

    var newInput = document.createElement("input");

    newInput.type = "file";
    newInput.id = oldInput.id;
    newInput.name = oldInput.name;
    newInput.className = oldInput.className;
    newInput.style.cssText = oldInput.style.cssText;
    // copy any other relevant attributes

    oldInput.parentNode.replaceChild(newInput, oldInput);
}