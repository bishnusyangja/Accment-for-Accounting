$(document).ready(function () {

    vm = new CategoryViewModel();
    ko.applyBindings(vm);
});

function CategoryViewModel(){
     var self = this;

    self.particulars = new TableViewModel({}, CategoryRowViewModel);

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
            url: '/ledger/save/multiple-category/',
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

function CategoryRowViewModel() {

    var self = this;
    self.name = ko.observable();

    self.parent = ko.observable();

    self.validate = function(){
        if(!self.name()){
            bs_alert.error("Name is Required!");
            return false;
        }
        else if(!self.parent()){
            bs_alert.error("Parent Category is Required!");
            return false;
        }
        else{
            return true;
        }
    }
}
