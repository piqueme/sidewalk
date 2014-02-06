$(document).ready(function()
{
    $.ajaxSetup ({
        cache: false
    });
    $window = $(window);
 
    $('section[data-type="background"]').each(function()
    {
        var $scroll = $(this);
                         
        $(window).scroll(function() 
        {                 
            var yPos = -($window.scrollTop() / $scroll.data('speed')); 
            var coords = '50% '+ yPos + 'px';
     
            $scroll.css({ backgroundPosition: coords });    
        }); 
    }); 

    startParallaxScrolling();
    hideAllAlerts();
    startLoginFormAjaxListener();
    startRegisterFormAjaxListener();
}); 

function startParallaxScrolling() 
{
    $('a[href*=#]:not([href=#])').click(function() 
    {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) 
        {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
                $('html,body').animate(
                {
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
}

function hideAllAlerts()
{
    $(".alert").hide();
}

function clearLoginFormInputs() 
{
    $(":input", "#login-form")
     .not(":button, :submit, :reset, :hidden")
     .val('')
     .removeAttr('checked')
     .removeAttr('selected');
}

 
function clearRegistrationFormInputs() 
{
    $(":input", "#register-form")
     .not(":button, :submit, :reset, :hidden")
     .val('')
     .removeAttr("checked")
     .removeAttr("selected");
}


function startLoginFormAjaxListener()
{
    $("#login-form").ajaxForm(
    {
        beforeSubmit: function()
        {
            hideAllAlerts();
        },
        uploadProgress: function(event, position, total, percentComplete)
        {
            // draw loading circle
        },
        success: function(response)
        {
            clearLoginFormInputs();
            handleLoginCheckResponse(response);
        },
        error: function()
        {
            handleLoginPostError();
        }
    });
}

function startRegisterFormAjaxListener()
{
    $("#register-form").ajaxForm(
    {
        beforeSubmit: function()
        {
            hideAllAlerts();
        },
        uploadProgress: function(event, position, total, percentComplete)
        {
            // draw loading circle
        },
        success: function(response)
        {
            handleRegistrationCheckResponse(response);
        },
        error: function()
        {
            handleRegisterPostError();
        }
    });
}
function handleLoginCheckResponse(response) 
{
    if (response === "bad_login")
    {
        displayBadLoginBox();
    }
    else if (response === "success")
    {
        window.location = "../dash";
    }
    else
    {
        $("#section0").prepend(response);
    }
}

function handleRegistrationCheckResponse(response) 
{
    var response_text_array = response.split("&");
    var other_error = 1;
    if (response_text_array[0] === "user_exists")
    {
        displayRegisterError("user_exists");
        other_error = 0;
    }
    if (response_text_array[1] === "email_exists")
    {
        displayRegisterError("email_exists");
        other_error = 0;
    }
    if (response_text_array[2] === "verify_password_fail")
    {
        displayRegisterError("verify_password_fail");
        other_error = 0;
    }
    if (response_text_array[3] === "verify_email_fail")
    {
        displayRegisterError("verify_email_fail");
        other_error = 0;
    }
    if (response_text_array[4] === "not_agree")
    {
        displayRegisterError("not_agree");
        other_error = 0;
    }
    if (response_text_array[5] === "invalid_user")
    {
        displayRegisterError("invalid_user");
        other_error = 0;
    }
    if (response === "success")
    {
        window.location = "../dash";
        other_error = 0;
    }
    if (other_error === 1)
    {
        $("button[name=registration]").after(response);
    }
}


function handleLoginPostError()
{
    $("#login-error-alert").show();
}

function handleRegisterPostError()
{
    $("#register-error-alert").show();
}

function displayBadLoginBox()
{
    $("#bad-login-alert").show();
}

function displayRegisterError(responseText)
{
    if (responseText === "user_exists")
    {
        $("#user-exists-alert").show();
    }
    else if (responseText === "email_exists")
    {
        $("#email-exists-alert").show();
    }
    else if (responseText === "verify_password_fail")
    {
        $("#verify-password-alert").show();
    }
    else if (responseText === "verify_email_fail")
    {
        $("#verify-email-alert").show();
    }
    else if (responseText === "not_agree")
    {
        $("#notagree-alert").show();
    }
    else if (responseText === "invalid_user")
    {
        $("#baduname-alert").show();
    }
}
