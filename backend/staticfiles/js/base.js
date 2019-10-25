$(document).ready(function() {
    $("#signupForm").submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/',
            data:{
                email: $('#id_email').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success: function(json){
                console.log("Signup success")
                document.getElementById("signupForm").reset();
                $("#returnmessage").html('<p>Allemaal gelukt! :-) Email: ' + json.email + '</p>')
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
})
