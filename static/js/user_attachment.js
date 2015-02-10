$(document).ready(function () {
    //vm = new DayJournal(ko_data);
    //ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');

    $('#clear-other-attachment').on('click', function(){
        clearFileInput("other-attachment");
    });

    $('#clear-sales-attachment').on('click', function(){
        clearFileInput("sales-attachment");
    });

    $('#clear-bank-attachment').on('click', function(){
        clearFileInput("bank-attachment");
    });

    $('#clear-purchase-attachment').on('click', function(){
        clearFileInput("purchase-attachment");
    });

    if (window.location.hash != "") {
        $('a[href="' + window.location.hash + '"]').click();
    }
    $(document).on("click", ".delete-attachment", function (e) {
        e.preventDefault();
        var $this = $(this);
        if (confirm("Are you sure you want to delete this attachment?")) {
            var uri = build_attachment_url($this.data("type"), $this.data('id'));
            $.post(uri.url, uri.params)
                .done(function (res) {
                    if (res.success) {
                        $this.parent('.span3').fadeOut(300, function () {
                            $(this).remove();
                        });
                    } else {
                        alert("There has been error while processing your request. Please try again!");
                    }
                });
        } else {
            return false;
        }
    });

    function build_attachment_url(type, id) {
        return {url: "/user/delete_user_attachments/", params: {type: type, id: id}};
    }

    var add_file_view = $('.attach_file_field').first();

    $('.add_file').click(function () {
        var _parent = $(this).parent('p');
        var clone = add_file_view.clone();
        clone.append('<button type="button" class="btn btn-danger pull-right remove-file-attach">X</button>')
        clone.find('input').val("");
        _parent.before(clone);
    });

    $(document).on('click', '.remove-file-attach', function () {
        $(this).parent('.attach_file_field').slideUp(400, function () {
            $(this).remove()
        });
    });

    $('.attachment-form').submit(function (e) {
        e.preventDefault();
        if (window.FormData) {
            var file_ips = $(this).find('input[type="file"]');
            var text_ips = $(this).find('.captions');
            var formdata = new FormData();
            $.each(text_ips, function () {
                formdata.append("captions", this.value);
            });
            $.each(file_ips, function () {
                formdata.append("attachments", this.files[0]);
            });
            var $this = $(this);
            var type = $this.data("type");
            formdata.append("type", type);
            formdata.append("day", $('#attachment_tabbable').data("journal-day"));

            $.ajax({
                url: "/user/save_user_attachments/",
                type: "POST",
                data: formdata,
                processData: false,
                contentType: false,
                success: function (res) {
                    var str = "";
                    $.each(res, function () {
                        str += '<div class="span3"> <a target="_blank" href="' + this.link + '">' + this.caption + '</a><button class="close delete-attachment" data-type="' + type + '" data-id="' + this.id + '"><span class="icon-trash"></span></button></div>';
                    });
                    $this.find('.row-fluid').append(str);
                    $this.find('.attach_file_field').find("input").val("").end().not(':first').remove();
                    bs_alert.success('saved!');
                    clear_alert(2000);

                },
                error: function () {
                    alert("There has been error while processing your request. Please try again!");
                }
            });

        } else {
            alert("Your browser is too old. Please upgrade to modern browsers like Chrome or Firefox.")
        }
    });

});


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


function clear_alert(x)
{
setTimeout(function(){bs_alert.clear();},x);

}
