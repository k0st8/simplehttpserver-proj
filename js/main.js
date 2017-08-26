$(document).ready(function(){
     function readFile(){
        console.log('Reading file....');
        $.ajax({
          'type' : 'GET',
          'dataType' : 'json',
          'url' : 'http://localhost:8000/data/info.txt',
          'statusCode' : {
            404: function(){
                let msg = 'File not found';
                console.log(msg);
                $('#message').append('<li>' + msg + '</li>');
            }
          },
          'success': function(data) {
            //do something
            console.log("Success Reading!");
            var ul = $('#message');
            ul.empty();
            $.each(data, function(i, obj){
                ul.append('<li>User: ' + obj.user + '; IP:' + obj.ip + '</li>');
            });
          }

        });
    };
    // First time
    readFile();


    /// Save new user to the file
    $("#save").click(function(e){
        e.preventDefault();
        var res = {};
        var d = JSON.stringify($('form').serializeArray().map(function(x){res[x.name] = x.value;}));
        $.ajax({
          'type' : 'POST',
          'dataType' : 'json',
          'url' : 'http://localhost:8000',
          'data': res,
          'success': function(data) {
            //do something

          },

          complete: function(){
            // Cleaning fields from data
            var resetFields = $('form').find('.reset');
            $.each(resetFields, function(i, val){
                $(val).val('');
            });
                // Read file info.txt
                readFile();
          }
        });
    });


});