//var rate = $('#rating-value').value;
//$('#quest-rating').raty({ 
//    readOnly: true, 
//    score: rate,
//    starHalf: '../images/star-icon-half.png',
//    starOff: '../images/star-icon-off.png',
//    starOn: '../images/star-icon-on.png'
//})

$(document).ready(function() {
    //$('#thumbnail-viewer').carousel();
    $.ajaxSetup ({
        cache: false
    });
    createCompletionModalListener(); 
    hideAllAlerts();
    forfeitFormListener();
    acceptFormListener();
    removeFormListener();
});

function hideAllAlerts()
{
    $(".alert").hide();
}

function forfeitFormListener() {
    var forfeit_url = "forfeit";
    $('#forfeit-button-form').ajaxForm(
    {
        beforeSubmit: function()
        {
            hideAllAlerts();
        },
        uploadProgress: function()
        {
            // in the case of progress
        },
        success: function(response) 
        {
            handleForfeitResponse(response);
        },
        data: {submit: true}
    });
}

function removeFormListener() {
    var remove_url = "remove";
    $('#remove-button-form').ajaxForm(
    {
        beforeSubmit: function()
        {
            hideAllAlerts();
        },
        uploadProgress: function()
        {
            // in the case of progress
        },
        success: function(response) 
        {
            handleRemoveResponse(response);
        },
        data: {submit: true}
    });
}

function acceptFormListener() {
    var accept_url = "accept";
    $('#accept-button-form').ajaxForm(
    {
        beforeSubmit: function()
        {
            hideAllAlerts();
        },
        uploadProgress: function()
        {
            // in the case of progress
        },
        success: function(response) 
        {
            handleAcceptResponse(response);
        },
        data: {submit: true}
    });
}



function handleForfeitResponse(response) 
{
    if (response === "success") {
        displayMessage("forfeit-success");
    }

    if (response === "already-forfeited") {
        displayMessage("forfeit-error");
    }
}

function handleAcceptResponse(response) 
{
    if (response === "success") {
        displayMessage("accept-success");
    }
    if (response === "already-accepted") {
        displayMessage("accept-error")
    }
}

function handleRemoveResponse(response) 
{
    if (response === "success") {
        location.href = "../../dash"
        $("#quest.content-panel").before("<div id='remove-success' class='alert alert-success'> <strong> Hooray </strong> You successfully deleted this quest! </div>");
        $('#remove-success').show();
    }   
}

function displayMessage(responseText) 
{
    if (responseText === "forfeit-success")
    {
        $('#forfeit-button').hide();
        $("#forfeit-success-alert").slideToggle();
        $('#complete-button').hide();
        $('#accept-button').fadeIn();
    }

     if (responseText === "forfeit-error")
     {
         $("#forfeit-error-alert").show();
     }

    if (responseText === "accept-success")
    {
        $('#accept-button').hide();
        $('#accept-success-alert').slideToggle();
        $('#complete-button').fadeIn();
        $('#forfeit-button').fadeIn();
    }

     if (responseText === "accept-error")
     {
         $('#accept-error-alert').show();
     }

    if (responseText === "remove-success")
    {
        $('#remove-success-alert').fadeIn();
    }
}

function createCompletionModalListener() {
    $('#complete-button').click(function(event)
    {
        $('#quest-complete-dialog').modal();
        createCompletionFormListener(); 
    });
}

function createCompletionFormListener() {
    var completion_url = "complete";
    var options = {
        dataType: 'html',
        url: completion_url,
        beforeSubmit: showRequest,
        success: showResponse 
    }
    //$('#completion-form').ajaxSubmit(options);
    $('#completion-form').ajaxForm( 
    {
        beforeSubmit: function()
        {
            removeAllAlerts();
        },
        uploadProgress: function(event, position, total, percentComplete)
        {
            // draw loading circle
        },
        success: function(response)
        {
            showResponse(response);
        },
        error: function()
        {
            handleCompletionError();
        }
    });
}

function showRequest() {
    // do something with form data
    return True;
}

function clearFormInputs() {
    $(':input','#completion-form')
      .not(':button, :submit, :reset, :hidden')
      .val('')
      .removeAttr('checked')
      .removeAttr('selected');
}

function showResponse(response) {
    if (response === "success")
    {
        $("#quest-complete-dialog").modal('hide');
        $('#forfeit-button').hide();
        $('#complete-button').hide();
        $('#accept-button').hide();
        $('#completed-tag').fadeIn();
        $("#quest-content-panel").before("<div class='alert alert-success'> <strong> Hooray </strong> You completed the quest! </div>");
    }
    else
    {
        $("#cquest-content-panel").before(response);
    }
}

function hideAllAlerts() {
    $(".alert").hide();
}

function removeAllAlerts() {
    $(".alert").remove();
}

function handleCompletionError() {
    $("#quest-content-panel").before("<div class='alert alert-danger'> <strong> Oh no! </strong> There was a connection problem! </div>");
}

function checkImageUploads() {
    
}
// Add verification minipage for completion
// Add accept quest communication with backend
// Add remove quest communication with backend

// Add javascript for adding challenge
//
//
//
// Add javascript for loading completed photos (21)
// Add javascript for scrolling to side
