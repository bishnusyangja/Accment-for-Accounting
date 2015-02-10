function search_watson(search_link, account){
        account = account || null;
        $("#search-box").keyup(function(){
           var text = $("#search-box").val();
           if (text == ''){
             $("#results").attr("class", 'hidden');
           }else{
             $("#results").removeAttr("class");
           }
           $.ajax({
                    type: "POST",
                    url: search_link,
                    dataType:"html",
                    data: {'text':text,'account':account},
                    success: function(datas){
                        var datas = $.parseJSON(datas);
                        if(datas.length>0){
                            $("#search-results").empty();
                            for(var i=0;i<datas.length;i++){
                            var temp_link = datas[i]['url'];
                            var temp_title = datas[i]['title'];
                            var tem = "<tr><td><a href=' " + temp_link + " ' "+ ">";
                            var temp = tem + temp_title + "</a></td></tr>";
                            $("#search-results").append(temp);
                            }
                        }
                        else{
                        $("#search-results").empty();
                        $("#search-results").html("<b>No results to Show</b>");
                        }

                    }
                })
           });
}
