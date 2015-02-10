$(document).ready(function () {

    vm = new AccountViewModel();
    ko.applyBindings(vm);
});

function AccountViewModel(){
     var self = this;

    self.particulars = new TableViewModel({}, AccountRowViewModel);

    $.ajax({
        url: '/ledger/categories.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.categories = data;
        }
    });

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

    self.our_save = function(){
            if(!self.validate()){
                return;
            }

        $.ajax({
            type: "POST",
            url: '/ledger/save/multiple-account/',
            data: ko.toJSON(self),
            async: false,
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    bs_alert.error(msg.error_message);
                }
                else {
                    bs_alert.success('Saved!');

                }
            }
        });
 }

}

function AccountRowViewModel() {

    var self = this;
    self.name = ko.observable();

    self.category = ko.observable();
    self.opening_dr = ko.observable();
    self.opening_cr = ko.observable();

    self.validate = function(){
        if(self.opening_dr() && self.opening_cr()){
            bs_alert.error("Both Debit and Credit amount are not allowed!");
            return false;
        }
        else if(!self.name()){
            bs_alert.error("Name is Required!");
            return false;
        }
        else if(!self.category()){
            bs_alert.error("Category is Required!");
            return false;
        }
        else{
            return true;
        }
    }
}
