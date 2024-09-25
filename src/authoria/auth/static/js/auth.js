function authRequest(csrf_token, auth_type){
    // Set default configuration
    action_button_stock_html = $(".action-button").html();
    $('.messages').empty();
    $(".action-button").html(loadingSpinner());

    // Collect auth data
    auth_data = {}
    if (auth_type == 'login') {
        auth_data['username_or_email'] = $('#username_or_email').val().toLowerCase();
        auth_data['password'] = $('#password').val();
    }
    else if (auth_type == 'signup') {
        auth_data['username'] = $('#username').val().toLowerCase();
        auth_data['email'] = $('#email').val().toLowerCase();
        auth_data['password'] = $('#password').val();
        auth_data['password-confirm'] = $('#password-confirm').val();
    }
    auth_data['timezone'] = Intl.DateTimeFormat().resolvedOptions().timeZone;

    // Validate auth data
    var validation_errors = authDataValidation(auth_data);
    if (validation_errors.length > 0) {
        $(".action-button").html(action_button_stock_html);
        compileValidationErrorMessages(validation_errors);
    } else {
        sendAuthData(csrf_token, auth_data);
    }
}

function sendAuthData(csrf_token, auth_data) {
    $.ajax({
        type: "POST",
        url: "",
        data: {
            csrfmiddlewaretoken: csrf_token,
            auth_data: JSON.stringify(auth_data),
        },

        success: function(response){
            location.reload();
        },

        error: function(response){
            $(".action-button").html(action_button_stock_html);
            exceptionsHandler(response.responseJSON);
        }
    });

    return false;
}